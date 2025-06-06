import pandas as pd
import io
import re
from PIL import Image
from transformers import VisionEncoderDecoderModel, DonutProcessor
from app.utils.transform import str_to_int, extract_int

processor = DonutProcessor.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2")


def postprocess_qcap(qcap_out: dict):
    """
    Konversi output mentah dari QCap menjadi struktur baku untuk klasifikasi QRep.

    Args:
        qcap_out (dict): Output mentah dari QCap.

    Returns:
        Tuple[pd.DataFrame, dict]: DataFrame menu dan metadata transaksi.
    """
    menu_raw = qcap_out.get("menu", [])
    df = pd.DataFrame(menu_raw)

    df.rename(columns=lambda x: x.strip().lower(), inplace=True)
    df.rename(columns={"nm": "item", "cnt": "qty"}, inplace=True)

    # Konversi qty dan price ke int
    df['qty'] = df['qty'].apply(lambda x: int(
        x) if isinstance(x, int) else extract_int(str(x)))
    df['price'] = df['price'].apply(lambda x: int(
        x) if isinstance(x, int) else str_to_int(str(x)))

    metadata = {
        "merchant_name": qcap_out.get("merchant", ""),
        "date": qcap_out.get("date", ""),
        "total_amount": str_to_int(qcap_out.get("total", {}).get("total_price", 0)),
        "payment_method": qcap_out.get("pembayaran", "")
    }

    return df, metadata


def process_qcap(image_bytes: bytes) -> dict:
    """
    Ekstraksi data dari gambar struk menggunakan Donut (OCR + NER).

    Args:
        image_bytes (bytes): Gambar dalam bentuk bytes (dari UploadFile).

    Returns:
        dict: Hasil ekstraksi dalam format dictionary.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Gagal membuka gambar: {e}")

    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(
        task_prompt, add_special_tokens=False, return_tensors="pt"
    ).input_ids

    pixel_values = processor(image, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values=pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=model.decoder.config.max_position_embeddings,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(
        processor.tokenizer.pad_token, ""
    )
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
    return processor.token2json(sequence)

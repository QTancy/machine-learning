import pandas as pd
import io
import re
from PIL import Image
from transformers import VisionEncoderDecoderModel, DonutProcessor
from app.utils.transform import str_to_int, extract_int, parse_item_string_fallback
from app.schemas.response import QCapItem

processor = DonutProcessor.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained(
    "naver-clova-ix/donut-base-finetuned-cord-v2")


def postprocess_qcap(qcap_out: dict) -> dict :
    """
    Konversi output mentah dari QCap menjadi struktur baku untuk klasifikasi QRep.

    Args:
        qcap_out (dict): Output mentah dari QCap.

    Returns:
        dict: Hasil ekstraksi dalam format dictionary yang cocok dengan QCapResponse.
    """
    menu_raw = qcap_out.get("menu", [])

    
    if isinstance(menu_raw, dict):
        print(f"Info: Donut 'menu' output berupa sebuah dictionary. Masukkan didalam list untuk diolah. Value: {menu_raw}")
        menu_raw = [menu_raw] 
    elif isinstance(menu_raw, str):
        if menu_raw.strip(): 
            print(f"Info: Donut 'menu' output berupa sebuah string. Masukkan didalam list untuk diolah pakai fallback. Value: {menu_raw}")
            menu_raw = [menu_raw] 
        else:
            menu_raw = [] 
    elif not isinstance(menu_raw, list):
        print(f"Warning: Donut 'menu' output bukan list, dictionary atau string. Tipe Datanya: {type(menu_raw)}, Value: {menu_raw}. Ubah ke list kosong!.")
        menu_raw = []
    
    
    processed_menu_items = []
    for item_data in menu_raw:
        # Data yang dictionary
        if isinstance(item_data, dict):
            kuantitas_val = item_data.get("cnt", 0)
            harga_val = item_data.get("price", 0)
            processed_menu_items.append(QCapItem( 
                nama=item_data.get("nm", ""),
                kuantitas=int(kuantitas_val) if isinstance(kuantitas_val, int) else extract_int(str(kuantitas_val)),
                harga=int(harga_val) if isinstance(harga_val, int) else str_to_int(str(harga_val)) 
            ).model_dump())
        # Data yang string (biasanya kalau cuman 1 item saja)
        elif isinstance(item_data, str):
            parsed_item = parse_item_string_fallback(item_data) 
            processed_menu_items.append(QCapItem(**parsed_item).model_dump()) 
        else:
            print(f"Warning: Skip,karena tidak sesuai tipe datanya. Tipe Datanya : {type(item_data)}, Value: {item_data}")
            continue
        
    toko_val = qcap_out.get("merchant", "")
    tanggal_val = qcap_out.get("date", "")

    donut_sub_total_dict = qcap_out.get("sub_total", {}) 

    
    sub_total_raw = donut_sub_total_dict.get("subtotal_price", "0") 
    pajak_raw = donut_sub_total_dict.get("tax_price", "0")       
    dll_raw = qcap_out.get("etc", "0") 

    total_harga_raw = qcap_out.get("total", {}).get("total_price", "0")
    total_harga_int = str_to_int(str(total_harga_raw))
    sub_total_int = str_to_int(str(sub_total_raw)) 
    pajak_int = str_to_int(str(pajak_raw))        
    dll_int = str_to_int(str(dll_raw)) 

    total_harga_dict_for_pydantic = {"total_price": total_harga_int}

    
    final_response_dict = {
        "toko": toko_val,
        "tanggal": tanggal_val,
        "item": processed_menu_items, 
        "total_harga": total_harga_dict_for_pydantic,
        "sub_total": sub_total_int,
        "pajak": pajak_int,
        "dll": dll_int,
    }


    return final_response_dict


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

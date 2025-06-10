from fastapi import APIRouter, UploadFile, File
from app.schemas.response import QCapResponse, QRepReportResponse
from app.services.qcap import process_qcap, postprocess_qcap
from app.services.qrep import classify_qrep

router = APIRouter()

# ------------------ QCAP: Upload ------------------


@router.post("/qcap/upload", response_model=QCapResponse)
async def qcap_upload(file: UploadFile = File(...)):
    """
    Menerima gambar struk via multipart/form-data, lalu melakukan OCR + NER.
    Return hasil ekstraksi toko, tanggal, item, total_harga.
    """
    image_bytes = await file.read()
    raw_qcap_output = process_qcap(image_bytes)
    final_qcap_response = postprocess_qcap(raw_qcap_output)
    return final_qcap_response


# ------------------ QREP: Classify (from QCap output) ------------------

@router.post("/qrep/classify", response_model=QRepReportResponse)
def qrep_classify_from_qcap(qcap_result: dict):
    """
    Menerima hasil QCap (OCR dalam format dict), lalu melakukan klasifikasi kategori item.
    """
    return classify_qrep(qcap_result)

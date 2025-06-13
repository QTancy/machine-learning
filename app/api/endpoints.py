from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from typing import List, Literal

from app.schemas.response import QCapResponse, QRepReportResponse
from app.schemas.database_models import StrukDatabaseModel, ClassifiedReceiptItem
from app.services.qcap import process_qcap, postprocess_qcap
from app.services.qrep import classify_qrep
from app.database.database import create_db_and_tables, get_db
from app.api.dependencies import get_current_user_id 
from app.utils.crud import create_receipt_with_items, get_receipts_by_user


router = APIRouter()

# @router.lifespan("startup")
# async def startup_event():
#     await create_db_and_tables()

# ------------------ QCAP: Upload ------------------


@router.post("/qcap/upload", response_model=QCapResponse)
async def qcap_upload(file: UploadFile = File(...), metode_pembayaran : str = Form('Tidak Diketahui')):
    """
    Menerima gambar struk via multipart/form-data, lalu melakukan OCR + NER.
    Return hasil ekstraksi toko, tanggal, item, total_harga.
    """
    image_bytes = await file.read()
    raw_qcap_output = process_qcap(image_bytes)
    final_qcap_response = postprocess_qcap(raw_qcap_output)
    final_qcap_response['metode_pembayaran'] = metode_pembayaran
    return final_qcap_response


# ------------------ QREP: Classify (from QCap output) ------------------

@router.post("/qrep/classify", response_model=QRepReportResponse)
def qrep_classify_from_qcap(qcap_data: QCapResponse): # <--- Menerima QCapResponse LANGSUNG!
    """
    Menerima hasil QCap yang sudah lengkap (dalam format QCapResponse),
    lalu melakukan klasifikasi kategori item.
    """
    # Tidak perlu try-except untuk QCapResponse(**qcap_result)
    # karena FastAPI sudah memvalidasinya saat menerima qcap_data.

    # Langsung panggil fungsi klasifikasi, meneruskan objek QCapResponse
    report_response = classify_qrep(qcap_data)

    return report_response

# ------------------ QCAP+QREP: PROCESS SEMUANYA (QCAP+QREP) ------------------
@router.post("/qcap/upload_and_process_all", response_model=QRepReportResponse)
async def qcap_upload_and_process_all(
    file: List[UploadFile] = File(...),
    metode_pembayaran: str = Form('Kredit'),
    bahasa : Literal['ID','US'] = Form("US"),
    current_user_id: int = Depends(get_current_user_id), 
    db: AsyncSession = Depends(get_db)
):
    """
    Menerima gambar struk dan metode pembayaran,
    melakukan OCR, ekstraksi, klasifikasi item, dan menyimpan hasilnya ke database,
    terkait dengan user yang terautentikasi.
    Mengembalikan laporan QRep akhir.
    """
    processed_reports = []
    for fil in file : 
        try:
            image_bytes = await fil.read()
            raw_qcap_output = process_qcap(image_bytes)
            extracted_data_from_ocr_dict = postprocess_qcap(raw_qcap_output,locale=bahasa)
            extracted_data_from_ocr_dict['metode_pembayaran'] = metode_pembayaran

            qcap_data_validated = QCapResponse(**extracted_data_from_ocr_dict)
            report_response = classify_qrep(qcap_data_validated)

            
            classified_items_for_db = []
            for item_report in report_response.item:
                classified_items_for_db.append(
                    ClassifiedReceiptItem(
                        nama=item_report.nama,
                        kuantitas=item_report.kuantitas,
                        harga=item_report.harga,
                        kategori=item_report.kategori
                    )
                )

            db_data = StrukDatabaseModel(
                user_id = current_user_id,
                toko=report_response.toko,
                tanggal_transaksi=report_response.tanggal, 
                total_harga=report_response.total_harga,
                metode_pembayaran=report_response.metode_pembayaran,
                items=classified_items_for_db, 
                tanggal_proses=datetime.now(),
                sub_total_pajak=qcap_data_validated.sub_total.pajak, 
                sub_total_dll=qcap_data_validated.sub_total.dll      
            )
            created_receipt = await create_receipt_with_items(db, current_user_id, db_data)
            processed_reports.append(report_response)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal server: {e}")
    return processed_reports
    

# ------------------ SEMUA DATA STRUK YANG PERNAH DIPROSES ------------------
@router.get("/receipts/my_receipts", response_model=List[StrukDatabaseModel])
async def get_my_receipts(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    try:
        receipts_from_db = await get_receipts_by_user(db, current_user_id)
        validated_receipts_for_response = []
        for receipt_orm in receipts_from_db: 
            classified_items_list = []
            if receipt_orm.items: 
                for item_orm in receipt_orm.items:
                    classified_items_list.append(
                        ClassifiedReceiptItem(
                            nama=item_orm.nama,
                            kuantitas=item_orm.kuantitas,
                            harga=item_orm.harga,
                            kategori=item_orm.kategori
                        )
                    )
            tanggal_str = ""
            
            if receipt_orm.tanggal_transaksi:
                tanggal_str = receipt_orm.tanggal_transaksi.strftime('%Y-%m-%d') if receipt_orm.tanggal_transaksi else ""
           

            # --- Buat instance StrukDatabaseModel ---
            pydantic_receipt = StrukDatabaseModel(
                id=receipt_orm.id,
                user_id=receipt_orm.user_id,
                toko=receipt_orm.toko,
                tanggal_transaksi=tanggal_str, 
                total_harga=receipt_orm.total_harga,
                sub_total_pajak=receipt_orm.sub_total_pajak,
                sub_total_dll=receipt_orm.sub_total_dll,
                metode_pembayaran=receipt_orm.metode_pembayaran,
                tanggal_proses=receipt_orm.tanggal_proses, 
                items=classified_items_list 
            )
            validated_receipts_for_response.append(pydantic_receipt)

        return validated_receipts_for_response

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Gagal mengambil data struk: {e}")
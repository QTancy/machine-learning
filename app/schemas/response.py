from pydantic import BaseModel
from typing import List


# ------------------ QCAP ------------------

class QCapItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int


class QCapResponse(BaseModel):
    toko: str
    tanggal: str
    item: List[QCapItem]
    total_harga: dict
    sub_total: int
    pajak: int
    dll: int


# ------------------ QREP REPORT ------------------

class QRepReportItem(BaseModel):
    item: str
    kuantitas: int
    harga: int


class QRepReportResponse(BaseModel):
    toko: str
    tanggal: str
    total_harga: int
    item_list: List[QRepReportItem]
    metode_pembayaran: str
    periode_laporan: str

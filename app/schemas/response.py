from pydantic import BaseModel
from typing import List

# ------------------ QCAP ------------------

class QCapItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int

class SubTotalDetails(BaseModel):
    pajak: int
    dll: int

class QCapResponse(BaseModel):
    toko: str
    tanggal: str
    item: List[QCapItem]
    total_harga: int
    sub_total: SubTotalDetails
    metode_pembayaran : str


# ------------------ QREP REPORT ------------------

class QRepReportItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int
    kategori : str


class QRepReportResponse(BaseModel):
    toko: str
    tanggal: str
    total_harga: int
    item: List[QRepReportItem]
    metode_pembayaran: str

from pydantic import BaseModel
from typing import List, Optional


class QRepItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int


class QRepClassifyRequest(BaseModel):
    toko: Optional[str] = ""
    tanggal: Optional[str] = ""
    metode_pembayaran: Optional[str] = ""
    periode_laporan: Optional[str] = "bulanan"
    item_list: List[QRepItem]

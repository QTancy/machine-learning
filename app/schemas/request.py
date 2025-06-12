from pydantic import BaseModel
from typing import List, Optional


class QRepItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int
    kategori : str


class QRepClassifyRequest(BaseModel):
    toko: Optional[str] = ""
    tanggal: Optional[str] = ""
    total_harga: Optional[int] = 0
    item: List[QRepItem]
    metode_pembayaran: Optional[str] = ""
    

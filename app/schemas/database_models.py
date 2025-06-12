from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime 

# Ini sama dengan QRepReportItem
class ClassifiedReceiptItem(BaseModel):
    nama: str
    kuantitas: int
    harga: int
    kategori: str


class StrukDatabaseModel(BaseModel):
    
    id: Optional[int] = None 
    user_id: int 
    toko: str
    tanggal_transaksi: str 
    total_harga: int
    sub_total_pajak: int 
    sub_total_dll: int   
    metode_pembayaran: str
    tanggal_proses: datetime = datetime.now() 
    items: List[ClassifiedReceiptItem]

    class Config:
        from_attributes = True 
        
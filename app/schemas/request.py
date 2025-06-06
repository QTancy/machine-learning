from pydantic import BaseModel
from typing import List, Optional


class QRepItem(BaseModel):
    name: str
    qty: int
    price: int


class QRepClassifyRequest(BaseModel):
    merchant: Optional[str] = ""
    date: Optional[str] = ""
    payment_method: Optional[str] = ""
    report_period: Optional[str] = "bulanan"
    items: List[QRepItem]

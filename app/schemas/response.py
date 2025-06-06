from pydantic import BaseModel
from typing import List


# ------------------ QCAP ------------------

class QCapItem(BaseModel):
    nm: str
    cnt: int
    price: int


class QCapResponse(BaseModel):
    merchant: str
    date: str
    menu: List[QCapItem]
    total: dict
    sub_total: int
    tax_price: int
    etc: int


# ------------------ QREP REPORT ------------------

class QRepReportItem(BaseModel):
    item: str
    qty: int
    price: int


class QRepReportResponse(BaseModel):
    merchant_name: str
    date: str
    total_amount: int
    item_list: List[QRepReportItem]
    payment_method: str
    report_period: str

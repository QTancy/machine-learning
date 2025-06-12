from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base 

class User(Base): 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String)    
    email = Column(String, unique=True, index=True, nullable=False) 
    password = Column(String) 
    created_at = Column(DateTime, default=func.now()) 

    receipts = relationship("Receipt", back_populates="owner")

class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    toko = Column(String, index=True, nullable=False)
    tanggal_transaksi = Column(DateTime, nullable=False)
    total_harga = Column(Integer, nullable=False)
    sub_total_pajak = Column(Integer, nullable=False)
    sub_total_dll = Column(Integer, nullable=False)
    metode_pembayaran = Column(String, nullable=False)
    tanggal_proses = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="receipts")
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")

class ReceiptItem(Base):
    __tablename__ = "receipt_items"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False) 
    nama = Column(String, nullable=False)
    kuantitas = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)
    kategori = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    receipt = relationship("Receipt", back_populates="items")
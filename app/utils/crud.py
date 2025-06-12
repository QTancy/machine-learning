from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.qtancy import Receipt, ReceiptItem 
from app.schemas.database_models import StrukDatabaseModel 
from app.utils.transform import convert_date_string_to_datetime

async def create_receipt_with_items(
    db: AsyncSession,
    user_id: int, # user_id bertipe int
    receipt_data: StrukDatabaseModel # Pydantic model dari database_models
) -> Receipt:
    
    parsed_tanggal_transaksi = convert_date_string_to_datetime(receipt_data.tanggal_transaksi)
    
    # Objek Receipt utama
    db_receipt = Receipt(
        user_id=user_id, 
        toko=receipt_data.toko,
        tanggal_transaksi=parsed_tanggal_transaksi, 
        total_harga=receipt_data.total_harga,
        sub_total_pajak=receipt_data.sub_total_pajak, 
        sub_total_dll=receipt_data.sub_total_dll,     
        metode_pembayaran=receipt_data.metode_pembayaran,
        tanggal_proses=receipt_data.tanggal_proses 
    )
  
    db.add(db_receipt)
    await db.flush() 

    for item_data in receipt_data.items:
        db_item = ReceiptItem(
            receipt_id=db_receipt.id,
            nama=item_data.nama,
            kuantitas=item_data.kuantitas,
            harga=item_data.harga,
            kategori=item_data.kategori
        )
        db.add(db_item)

    await db.commit()
    await db.refresh(db_receipt)
    return db_receipt

async def get_receipts_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    """
    Mengambil daftar struk berdasarkan user_id, dengan paginasi.
    """
    result = await db.execute(
        select(Receipt)
        .filter(Receipt.user_id == user_id)
        .options(selectinload(Receipt.items)) 
        .offset(skip)
        .limit(limit)
        .order_by(Receipt.tanggal_transaksi.desc()) 
    )
    
    return result.scalars().all()
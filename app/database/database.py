from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
from urllib.parse import urlparse 

DATABASE_URL = settings.DATABASE_URL

tmpPostgres = urlparse(DATABASE_URL)

DB_CONNECTION_STRING = (
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require"
)

engine = create_async_engine(DB_CONNECTION_STRING, echo=True) 
Base = declarative_base()

# AsyncSessionLocal: Digunakan untuk membuat sesi database
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False 
)

# Dependency untuk mendapatkan sesi database per request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Fungsi untuk membuat tabel (jalankan sekali saat deployment pertama)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
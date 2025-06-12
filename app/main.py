from contextlib import asynccontextmanager 
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
load_dotenv()
from app.api.endpoints import router
from app.database.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Creating database tables...")
    await create_db_and_tables()
    yield 
    print("Application shutdown: Performing cleanup...")
    

app = FastAPI(
    title="Qtancy ML Inference API",
    description="Backend for Qtancy",
    version="1.0.0",
    lifespan=lifespan,
    
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Qtancy API"}



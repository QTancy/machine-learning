from contextlib import asynccontextmanager 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "https://qtancy.netlify.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             
    allow_credentials=True,             
    allow_methods=["*"],               
    allow_headers=["*"],               
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Qtancy API"}



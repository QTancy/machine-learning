from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="Qtancy ML Inference API",
    description="Backend for Qtancy",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to Qtancy API"}

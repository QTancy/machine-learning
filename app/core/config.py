from pathlib import Path
from pydantic_settings import BaseSettings

# Path ke model klasifikasi kategori
QREP_PATH_TO_MODEL = Path("./models/qrep-model/model_bilstm.keras")

# Path ke file LabelEncoder
LE_PATH_TO_PKL = Path("./models/qrep-model/label_encoder.pkl")


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Capstone ML API"
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str 

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    

settings = Settings()

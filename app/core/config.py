from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar el .env general
dotenv_path = os.path.join(BASE_DIR, "security", ".env")
load_dotenv(dotenv_path, override=True)

# Cargar el .env para algorythm manualmente (opcional)
dotenv_alg_path = os.path.join(BASE_DIR, "security", "algorythm.env")
load_dotenv(dotenv_alg_path, override=True)

class Settings(BaseSettings):
    host: str
    portdb: str
    database: str
    user: str
    password: str

    class Config:
        env_file = dotenv_path

class SettingsAlgorythm(BaseSettings):
    secret_pkey: str
    algorythm: str
    expire_token: int

    class Config:
        env_file = dotenv_alg_path

settings = Settings()
setting_algorythm = SettingsAlgorythm()

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import FastAPI
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, "security", ".env")
load_dotenv(dotenv_path,override=True)

postgres_url = f"postgresql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}"

engine = create_engine(postgres_url)

def load_existing_db():
    SQLModel.metadata.create_all(engine)
    # SQLModel.metadata.reflect(engine)

def get_db():
    with Session(engine) as session:
        yield session

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialización
    load_existing_db()
    
    yield {
        "response": "Tables loaded successfully"
    }
    
    # Código de limpieza (opcional)
    print("Cerrando recursos de la aplicación")

SessionDep = Annotated[Session, Depends(get_db)]

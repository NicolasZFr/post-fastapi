from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.core.config import settings

postgres_url = f"postgresql://{settings.user}:{settings.password}@{settings.host}:{settings.portdb}/{settings.database}"

engine = create_engine(postgres_url)

def load_existing_db():
    SQLModel.metadata.reflect(engine)
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

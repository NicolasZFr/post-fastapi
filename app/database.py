from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import FastAPI
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os
dotenv_path = "./security/.env"
load_dotenv(dotenv_path,override=True)

postgres_url = f"postgresql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}"

engine = create_engine(postgres_url)

# Verifica si la BD existe (esto depende del motor de base de datos)
# def database_exists():
#     from sqlalchemy.engine import URL
#     from sqlalchemy_utils import database_exists, create_database

#     url = URL.create(postgres_url)
    
#     if not database_exists(url):
#         create_database(url)  # Crea la BD si no existe
#         return False  # Indica que la BD fue creada
#     return True  # Indica que la BD ya existía

# def create_db_and_tables():
#     """Crea las tablas solo si la BD no existía previamente."""
#     if not database_exists():
#         print("Creando base de datos y tablas...")
#         SQLModel.metadata.create_all(engine)  # Crea solo si la BD no existía
#     else:
#         print("La base de datos ya existe. Usándola sin modificarla.")

def load_existing_db():
    SQLModel.metadata.reflect(engine)

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

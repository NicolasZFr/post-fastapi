from fastapi import FastAPI, status, HTTPException, Query, Depends
from fastapi.params import Body
from fastapi.responses import Response

from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from datetime import datetime, timezone

from pydantic import BaseModel # Validar el tipo de dato que se recibe

from . import models
from .models import Post
from .database import SessionDep, load_existing_db, get_db, lifespan,engine#, create_db_and_tables

import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv
import os

import time

# Importar funciones de otro archivo
dotenv_path = "./security/.env"
load_dotenv(dotenv_path,override=True)

app = FastAPI(lifespan=lifespan, title='Posts with SQLModel')

# ------------------- Endpoints -------------------
# GET /posts --------------------------------------


@app.get("/")
async def root():
    return {"message": "Hello World, I'm Nicolás"}
# uvicorn app.main:app --reload

@app.get("/posts")
async def get_posts_list(session: SessionDep, Quantity: int = 10, Page: int = 1):
    query = select(Post).limit(Quantity).offset((Page - 1) * Quantity)
    posts = session.exec(query).all()  # Selecciona todos los registros de la tabla posts
    print(query.compile())
    ordered_posts = [
        {field: getattr(post, field) for field in Post.model_fields.keys()}
        for post in posts
    ]
    return {"data": ordered_posts}

@app.get("/posts/latest")
async def get_latest_post(session: SessionDep):
    query = select(Post).order_by(Post.id.desc())
    post = session.exec(query).first()  # Selecciona todos los registros de la tabla posts
    print(query.compile(engine))
    ordered_posts = {field: getattr(post, field) for field in Post.model_fields.keys()}
    return {"data": ordered_posts}

@app.get("/posts/{id}")
async def get_post_object(session: SessionDep,id:int):
    post = session.exec(select(Post).where(Post.id == id)).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
    
    ordered_posts = [
        {field: getattr(post, field) for field in Post.model_fields.keys()}
        for post in post
    ]
        
    return {"response": ordered_posts}


# POST /posts --------------------------------------
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(session: SessionDep, post: Post):
    provided_data = post.model_dump(exclude_unset=True)
    required_fields = ["title", "content", "rating"]
    missing_fields = [field for field in required_fields if field not in provided_data]

    # Si faltan campos, lanzar error con la lista de columnas
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    try:
        post.created_at = datetime.now(timezone.utc)  # Si quieres registrar fecha de creación
        session.add(post)
        session.commit()
        session.refresh(post)  # Obtiene los datos actualizados después del commit

        return {
            "response": f"Post '{post.title}' was created successfully",
            "data": {field: getattr(post, field) for field in Post.model_fields.keys()}
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



# DELETE /posts --------------------------------------
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")

    session.delete(post)
    session.commit()

    return Response(status_code=204)

# PUT /posts --------------------------------------
@app.put("/posts/{id}")
async def put_post(id: int, post: Post, session: SessionDep):
    existing_post = session.get(Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")

    post.id = id
    updated_data = post.model_dump()

    if any(value is None for value in updated_data.values()):
        missing_fields = [key for key, value in updated_data.items() if value is None]
        raise HTTPException(status_code=400, detail=f"Missing required fields: {missing_fields}")

    for key, value in updated_data.items():
        setattr(existing_post, key, value)

    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)

    return {"response": f"The post with id '{id}' was updated successfully", "data": {field: getattr(existing_post, field) for field in Post.model_fields.keys()}}
    
    
@app.patch("/posts/{id}")
async def patch_post(id: int, post: Post, session: SessionDep):
    existing_post = session.get(Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")

    updated_data = post.model_dump(exclude_unset=True)
    
    if not updated_data:
        raise HTTPException(status_code=400, detail="No data provided")

    for key, value in updated_data.items():
        setattr(existing_post, key, value)

    existing_post.updated_at = datetime.now(timezone.utc)  # Si quieres registrar fecha de actualización

    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)

    return {"response": f"The post with id '{id}' was updated successfully", "data": {field: getattr(existing_post, field) for field in Post.model_fields.keys()}}

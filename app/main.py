from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import Response

from sqlmodel import select
from datetime import datetime, timezone
from dotenv import load_dotenv

from . import models, schemas, utils
from .database import SessionDep, lifespan, engine#, create_db_and_tables
from .routers import post, user

app = FastAPI(
        lifespan=lifespan, 
        title='Posts with SQLModel', 
        description='API for managing posts and users', 
        version='1.0.0',
        openapi_tags=[
            {
                "name": "Post",
                "description": "Endpoints related to blog posts.",
            },
            {
                "name": "User",
                "description": "Operations related to user management."
            }
        ]
    )
app.include_router(post.router)
app.include_router(user.router)

# ------------------- Endpoints -------------------
# GET /posts --------------------------------------


@app.get("/")
async def root():
    return {"message": "Hello World, I'm Nicolás"}
# uvicorn app.main:app --reload
from fastapi import FastAPI

from app.infrastructure.databases.database import lifespan
from .routers import post, user, auth,vote

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
app.include_router(auth.router)
app.include_router(vote.router)

# ------------------- Endpoints -------------------
# GET /posts --------------------------------------


@app.get("/")
async def root():
    return {"message": "Hello World, I'm Nicolás"}
# uvicorn app.main:app --reload
# alembic revision -m "Initial migration"
from fastapi import status, HTTPException, Query, APIRouter

from sqlmodel import select

from .. import models, schemas, utils
from ..database import SessionDep, engine

router = APIRouter()

# ------------------- Endpoints -------------------

# GET /posts --------------------------------------
@router.get("/posts")
async def get_posts_list(session: SessionDep, Quantity: int = 10, Page: int = 1):
    query = select(models.Post).limit(Quantity).offset((Page - 1) * Quantity).order_by(models.Post.id.asc())
    posts = session.exec(query).all()  # Selecciona todos los registros de la tabla posts
    print(query.compile())
    ordered_posts = [
        {field: getattr(post, field) for field in models.Post.model_fields.keys()}
        for post in posts
    ]
    return {"data": ordered_posts}

@router.get("/posts/latest")
async def get_latest_post(session: SessionDep):
    query = select(models.Post).order_by(models.Post.id.desc())
    post = session.exec(query).first()  # Selecciona todos los registros de la tabla posts
    print(query.compile(engine))
    ordered_posts = {field: getattr(post, field) for field in models.Post.model_fields.keys()}
    return {"data": ordered_posts}

@router.get("/posts/{id}")
async def get_post_object(session: SessionDep,id:int):
    post = session.exec(select(models.Post).where(models.Post.id == id)).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
    
    ordered_posts = [
        {field: getattr(post, field) for field in models.Post.model_fields.keys()}
        for post in post
    ]
        
    return {"response": ordered_posts}


# POST /posts --------------------------------------
@router.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateResponse)
async def create_posts(session: SessionDep, post: schemas.PostCreate):
    required_fields = ["title", "content", "rating"]
    missing_fields = [field for field in required_fields if field not in post.model_dump(exclude_unset=True)]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )
    # Verifica si el post ya existe
    existing_post = session.exec(select(models.Post).where(models.Post.title == post.title,models.Post.content == post.content)).first()
    if existing_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with the same title and content already exists")
    post = models.Post(**post.model_dump())

    try:
        session.add(post)
        session.commit()
        session.refresh(post)  # Obtiene los datos actualizados después del commit

        return post

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )



# DELETE /posts --------------------------------------
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: SessionDep):
    post = session.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")

    session.delete(post)
    session.commit()

# PUT /posts --------------------------------------
@router.put("/posts/{id}")
async def put_post(id: int, post: schemas.PostCreate, session: SessionDep):
    existing_post = session.get(models.Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")

    updated_data = post.model_dump()

    if any(value is None for value in updated_data.values()):
        missing_fields = [key for key, value in updated_data.items() if value is None]
        raise HTTPException(status_code=400, detail=f"Missing required fields: {missing_fields}")

    for key, value in updated_data.items():
        setattr(existing_post, key, value)

    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)

    return {"response": f"The post with id '{id}' was updated successfully", "data": {field: getattr(existing_post, field) for field in models.Post.model_fields.keys()}}
    
# PATCH /posts --------------------------------------  
@router.patch("/posts/{id}")
async def patch_post(id: int, post: schemas.PostCreate, session: SessionDep):
    existing_post = session.get(models.Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")

    updated_data = post.model_dump(exclude_unset=True)
    
    if not updated_data:
        raise HTTPException(status_code=400, detail="No editable data provided")

    for key, value in updated_data.items():
        setattr(existing_post, key, value)

    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)

    return {"response": f"The post with id '{id}' was updated successfully", "data": {field: getattr(existing_post, field) for field in models.Post.model_fields.keys()}}
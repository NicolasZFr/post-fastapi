from fastapi import status, HTTPException, Query, APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlmodel import select,func
from typing import List

from app.infrastructure.model import Post, User, Vote
from app.schemas.post import *

from .. import oauth2
from app.infrastructure.databases.database import SessionDep, engine
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/api/posts", tags=["Post"], dependencies=[Depends(oauth2.get_current_user)])

# ------------------- Endpoints -------------------

# GET /posts --------------------------------------
@router.get("/", response_model=List[PostOrder])
async def get_posts_list(session: SessionDep, Quantity: int = None, Page: int = 1, user: User = Depends(oauth2.get_current_user), keyword: str = Query(default="", max_length=50, description="Palabra clave para buscar")):
    # query = select(Post).where(Post.content.contains(keyword))
    query = (
        select(Post, func.count(Vote.post_id).label("votes_count"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .where(Post.content.ilike(f"%{keyword}%"))
        .group_by(Post.id)
        .order_by(Post.id.asc())
    )
    if Quantity:
        query = query.limit(Quantity).offset((Page - 1) * Quantity)

    posts_with_votes = session.exec(query).all()

    results = [
        {
            **{field: getattr(post, field) for field in Post.model_fields.keys()},
            "user": session.exec(select(User).where(User.id == post.user_id)).first().model_dump(),
            "votes": votes
        }
        for post, votes in posts_with_votes
    ]

    return results

@router.get("/latest",response_model=PostOrder)
async def get_latest_post(session: SessionDep):
    query = (
        select(Post, func.count(Vote.post_id).label("votes_count"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .order_by(Post.id.desc())
    )
    latest_post, vote_count = session.exec(query).first()
    result = {
        **{field: getattr(latest_post, field) for field in Post.model_fields.keys()},
        "user": session.exec(select(User).where(User.id == latest_post.user_id)).first().model_dump(),
        "votes": vote_count
    }
    return result


@router.get("/{id}")
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
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=PostCreateResponse)
async def create_posts(session: SessionDep, post: PostCreate, user: User = Depends(oauth2.get_current_user)):
    required_fields = ["title", "content", "rating"]
    missing_fields = [field for field in required_fields if field not in post.model_dump(exclude_unset=True)]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )
    # Verifica si el post ya existe
    existing_post = session.exec(select(Post).where(Post.title == post.title,Post.content == post.content)).first()
    if existing_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post with the same title and content already exists")
    post = Post(user_id = user.id,**post.model_dump())  # Asigna el ID del usuario actual al nuevo post

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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: SessionDep, user: User = Depends(oauth2.get_current_user)):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id '{id}' not found")
    elif post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this post")

    session.delete(post)
    session.commit()

# PUT /posts --------------------------------------
@router.put("/{id}")
async def put_post(id: int, post: PostCreate, session: SessionDep, user: User = Depends(oauth2.get_current_user)):
    existing_post = session.get(Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")
    elif existing_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to modify this post")

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
    
# PATCH /posts --------------------------------------  
@router.patch("/{id}")
async def patch_post(id: int, post: PostCreate, session: SessionDep, user: User = Depends(oauth2.get_current_user)):
    existing_post = session.get(Post, id)

    if not existing_post:
        raise HTTPException(status_code=404, detail=f"Post with id '{id}' not found")
    elif existing_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to modify this post")

    updated_data = post.model_dump(exclude_unset=True)
    
    if not updated_data:
        raise HTTPException(status_code=400, detail="No editable data provided")

    for key, value in updated_data.items():
        setattr(existing_post, key, value)

    session.add(existing_post)
    session.commit()
    session.refresh(existing_post)

    return {"response": f"The post with id '{id}' was updated successfully", "data": {field: getattr(existing_post, field) for field in Post.model_fields.keys()}}
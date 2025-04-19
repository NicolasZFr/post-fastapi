from __future__ import annotations
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr, BaseModel
from app.schemas.user import UserOrder

class BasePost(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = True
    rating: float | None = None

class PostCreate(BasePost):
    pass

class PostCreateResponse(BasePost):
    created_at: datetime
    user_id: int | None = None

    class Config:
        from_attributes = True

class PostOrder(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    rating: float | None = None
    created_at: datetime
    updated_at: datetime | None = None
    user_id: int | None = None
    user: UserOrder
    votes: int | None = None

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    response: str
    data: PostOrder

    class Config:
        from_attributes = True

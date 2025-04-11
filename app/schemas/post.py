from __future__ import annotations
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr, BaseModel
from app.schemas.user import UserOut

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

class PostOut(BasePost):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    user_id: int | None = None
    user: UserOut

    class Config:
        from_attributes = True

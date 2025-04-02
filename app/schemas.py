from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr

class BasePost(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = True
    rating: float | None = None

class PostCreate(BasePost):
    pass

class PostCreateResponse(BasePost):
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str = Field(min_length=8, max_length=64)

class UserOut(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: str | None = None
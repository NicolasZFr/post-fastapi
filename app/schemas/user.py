from __future__ import annotations
from sqlmodel import Field
from datetime import datetime
from pydantic import EmailStr, BaseModel


class BaseUser(BaseModel):
    email: EmailStr

class UserCreate(BaseUser):
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str = Field(min_length=8, max_length=64)

class UserOut(BaseUser):
    id: int
    userrole_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseUser):
    password: str = Field(min_length=8, max_length=64)
from __future__ import annotations
from sqlmodel import Field
from datetime import datetime
from pydantic import EmailStr, BaseModel


class BaseUser(BaseModel):
    email: EmailStr
    # phone_number: str | None = None

class UserCreate(BaseUser):
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str = Field(min_length=8, max_length=64)

class UserOut(BaseUser):
    id: int
    # userrole_id: int

    class Config:
        from_attributes = True

class UserLogin(BaseUser):
    password: str = Field(min_length=8, max_length=64)


class UserOrder(BaseModel):
    id: int
    email: EmailStr
    # phone_number: str | None = None
    # userrole_id: int

    class Config:
        from_attributes = True
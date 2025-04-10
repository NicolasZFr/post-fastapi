from __future__ import annotations
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
from .database import SessionDep, get_db#,create_db_and_tables
from datetime import datetime, timezone
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from typing import Optional
from . import schemas
from sqlalchemy import text
from sqlalchemy import Column, TIMESTAMP

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}

    id: Optional[int] = Field(default=None,primary_key=True)
    title: str
    content: str
    published: bool = True
    rating: float | None = None

    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}, exclude=True)
    updated_at: datetime | None = Field(default=None,sa_column_kwargs={"onupdate": text("CURRENT_TIMESTAMP")}, exclude=True)
#     owner_id: int = Field(foreign_key="users.id")
#     owner: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default=None,
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
#     posts: list[Post] = Relationship(back_populates="owner")

# class Vote(SQLModel, table=True):
#     user_id: int = Field(foreign_key="users.id", primary_key=True)
#     post_id: int = Field(foreign_key="posts.id", primary_key=True)
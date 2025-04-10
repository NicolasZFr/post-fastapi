from __future__ import annotations
from datetime import datetime, timezone
from sqlmodel import Field, Session, SQLModel, Relationship
from typing import Optional, List
from app import schemas
from sqlalchemy import Column, TIMESTAMP, text, ForeignKey, Integer, orm
from sqlalchemy.orm import relationship

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
    user_id: int | None = Field(sa_column=Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"), nullable=True))

Post.model_rebuild()

Post.user = Relationship(back_populates="posts", sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "[Post.user_id]"})


# class Vote(SQLModel, table=True):
#     user_id: int = Field(foreign_key="users.id", primary_key=True)
#     post_id: int = Field(foreign_key="posts.id", primary_key=True)
from __future__ import annotations
from datetime import datetime, timezone
from sqlmodel import Field, Session, SQLModel, Relationship
from typing import Optional, List
from sqlalchemy import Column, TIMESTAMP, text, ForeignKey, Integer, orm, DateTime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post

class User(SQLModel, table=True):
    __tablename__ = "users"
    # __table_args__ = {"schema": "public"}

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default=None, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}, sa_type=DateTime(timezone=True), exclude=True)
    # phone_number: str | None = Field(default=None)
    # userrole_id: int = Field(default=2, sa_column=Column(Integer, ForeignKey("parametrics.userrole.id",name="fk_users_userrole_id", ondelete="SET DEFAULT")))
    # posts: List["Post"] = Relationship(back_populates="user")

# User.model_rebuild()

# User.posts = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

# class Vote(SQLModel, table=True):
#     user_id: int = Field(foreign_key="users.id", primary_key=True)
#     post_id: int = Field(foreign_key="posts.id", primary_key=True)
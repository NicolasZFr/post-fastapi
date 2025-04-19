from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, ForeignKey, Integer

class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}

    user_id: int | None = Field(sa_column=Column(Integer, ForeignKey("public.users.id"), nullable=True,primary_key=True))
    post_id: int | None = Field(sa_column=Column(Integer, ForeignKey("public.posts.id"), nullable=True,primary_key=True))
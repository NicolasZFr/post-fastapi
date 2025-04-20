from __future__ import annotations
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, ForeignKey, Integer

class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}

    post_id: int | None = Field(sa_column=Column(Integer, ForeignKey("public.posts.id",name="fk_votes_posts_id",ondelete="CASCADE",onupdate="CASCADE"), nullable=True,primary_key=True))
    user_id: int | None = Field(sa_column=Column(Integer, ForeignKey("public.users.id",name="fk_votes_users_id",ondelete="CASCADE",onupdate="CASCADE"), nullable=True,primary_key=True))
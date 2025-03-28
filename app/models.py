from .database import SessionDep, get_db#,create_db_and_tables
from datetime import datetime, timezone
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from typing import Optional


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}

    id: int = Field(default=None,primary_key=True)
    title: str
    content: str
    published: bool | None = True
    rating: float | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"server_default": "now()"}, exclude=True)
    updated_at: datetime | None = Field(default=None, sa_column_kwargs={"server_default": "now()"}, exclude=True)
    updated_at: Optional[datetime] = Field(default=None,sa_column_kwargs={"server_default": "now()", "onupdate": datetime.now(timezone.utc)},exclude=True)
#     owner_id: int = Field(foreign_key="users.id")
#     owner: Optional["User"] = Relationship(back_populates="posts")

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     email: str = Field(unique=True)
#     password: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     posts: list[Post] = Relationship(back_populates="owner")

# class Vote(SQLModel, table=True):
#     user_id: int = Field(foreign_key="users.id", primary_key=True)
#     post_id: int = Field(foreign_key="posts.id", primary_key=True)
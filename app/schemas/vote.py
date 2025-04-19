from __future__ import annotations
from pydantic import BaseModel,Field
from typing import Annotated
from pydantic.types import conint


class VoteBase(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, gt=0,le=1)]


class VoteResponse(BaseModel):
    response: str
    data: VoteBase
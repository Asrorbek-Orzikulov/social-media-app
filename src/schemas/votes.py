from typing import Literal
from pydantic import BaseModel


class VoteCreate(BaseModel):
    post_id: int
    vote: Literal[0, 1]


class VoteResponse(BaseModel):
    message: str

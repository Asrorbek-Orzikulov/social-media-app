from datetime import datetime
from pydantic import BaseModel

from .users import UserResponse


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostRecord(PostCreate):
    id: int
    created_at: datetime
    user: UserResponse


class PostResponse(BaseModel):
    Post: PostRecord
    vote_count: int

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


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


class TokenCreate(BaseModel):
    user_id: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class VoteCreate(BaseModel):
    post_id: int
    vote: Literal[0, 1]


class VoteResponse(BaseModel):
    message: str

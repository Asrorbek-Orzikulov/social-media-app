from datetime import datetime
from pydantic import BaseModel


class VideoCreate(BaseModel):
    user_id: int
    video_name: str
    video_content: bytes
    created_at: datetime


class VideoStatus(BaseModel):
    video_id: str
    status: str = "Success"

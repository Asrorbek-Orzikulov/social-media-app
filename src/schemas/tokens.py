from typing import Literal
from pydantic import BaseModel


class TokenVerified(BaseModel):
    user_id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

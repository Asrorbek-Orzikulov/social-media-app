from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from src import models, oauth2
from src.database.postgres import get_db
from src.utils import verify_password
from src.schemas.tokens import TokenResponse


router = APIRouter(prefix="/login", tags=["Authorization"])


@router.post("", response_model=TokenResponse)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    select_stmt = select(models.User).where(models.User.email == credentials.username)
    user_record = db.scalar(select_stmt)
    if user_record is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email and Password do not match!",
        )

    if not verify_password(credentials.password, user_record.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email and Password do not match!",
        )

    access_token = oauth2.create_access_token(data={"user_id": user_record.id})
    return {"access_token": access_token, "token_type": "bearer"}

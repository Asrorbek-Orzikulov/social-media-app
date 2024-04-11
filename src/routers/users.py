from sqlalchemy import select, update
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    select_stmt = select(models.User).where(models.User.email == user.email)
    user_record = db.scalar(select_stmt)
    if user_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists!",
        )

    user.password = hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("", response_model=schemas.UserResponse)
def get_user(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user

from datetime import datetime, timedelta, UTC

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, models
from .database import get_db
from .config import settings
from .utils import get_record


SECRET_KEY = settings.oauth_secret_key
ALGORITHM = settings.oauth_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.oauth_expiry_minutes
OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl="login")
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict) -> dict:
    data_to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    data_encoded = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return data_encoded


def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        return schemas.TokenVerified(user_id=user_id)
    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(OAUTH2_SCHEMA), db: Session = Depends(get_db)
):
    token_data = verify_access_token(token, CREDENTIALS_EXCEPTION)
    user_id = token_data.user_id
    user = get_record(db, models.User, "User ID", user_id)
    return user

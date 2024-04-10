from typing import Tuple, Optional

from fastapi import status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, database

pwd_context = CryptContext(schemes=["bcrypt"])


def get_record(
    db_session: Session,
    table: database.Base,
    primary_key_name: str | Tuple[str],
    primary_key: int | Tuple[int],
    raise_error: bool = True,
) -> Optional[database.Base]:
    if isinstance(primary_key_name, tuple) != isinstance(primary_key, tuple):
        raise ValueError(
            "primary_key_name and primary_key must both be tuples or neither."
        )

    if isinstance(primary_key_name, tuple) and (
        len(primary_key_name) != len(primary_key)
    ):
        raise ValueError(
            "The lengths of primary_key_name and primary_key must be the same."
        )

    record = db_session.get(table, primary_key)
    if raise_error and (record is None):
        if isinstance(primary_key_name, tuple):
            error_details = ", ".join(
                f"{name} {value}" for name, value in zip(primary_key_name, primary_key)
            )
        else:
            error_details = f"{primary_key_name} {primary_key}"

        error_message = f"Record with {error_details} not found!"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)

    return record


def verify_post_owner(post: models.Post, user: models.User):
    if post.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorized to modify the Post {post.id}!",
        )


def hash_password(password, pwd_context=pwd_context):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password, pwd_context=pwd_context):
    return pwd_context.verify(plain_password, hashed_password)

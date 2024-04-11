from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import status, Depends, APIRouter

from ..database import get_db
from .. import models, schemas, oauth2
from ..utils import get_record, verify_post_owner


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
):
    select_query = (
        select(models.Post, func.count(models.Vote.post_id).label("vote_count"))
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True,
        )
        .group_by(models.Post.id)
    )
    posts = db.execute(select_query).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(
    id: int,
    db: Session = Depends(get_db),
):
    post = get_record(db, models.Post, "Post ID", id)
    votes = db.scalar(
        select(func.count(models.Vote.post_id).label("vote_count"))
        .where(models.Vote.post_id == id)
        .group_by(models.Vote.post_id)
    )
    if votes is None:
        votes = 0
    return {"Post": post, "vote_count": votes}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRecord)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    deleted_post = get_record(db, models.Post, "Post ID", id)
    verify_post_owner(deleted_post, current_user)
    db.delete(deleted_post)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    updated_post = get_record(db, models.Post, "Post ID", id)
    verify_post_owner(updated_post, current_user)

    update_stmt = (
        update(models.Post).where(models.Post.id == id).values(**post.model_dump())
    )
    db.execute(update_stmt)
    db.commit()

from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src import models, oauth2
from src.database.postgres import get_db
from src.utils import get_record
from src.schemas.votes import VoteCreate, VoteResponse

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("", response_model=VoteResponse)
def vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    post_id = vote.post_id
    get_record(db, models.Post, "Post ID", post_id, raise_error=True)

    existing_vote = db.get(models.Vote, (user_id, post_id))
    if vote.vote == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user_id} has already voted for Post {post_id}",
            )
        new_vote = models.Vote(post_id=post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote successfully added!"}
    elif vote.vote == 0:
        if existing_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} has not voted for Post {post_id}",
            )
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote successfully removed!"}

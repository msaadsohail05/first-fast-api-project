from fastapi import APIRouter
from fastapi.params import Depends
from typing import Optional, List
from fastapi import  status,HTTPException, Depends, Response
from App import models, schema , oauth2
from App.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from passlib.context import CryptContext


router4 = APIRouter(prefix = "/votes",tags=["Votes"])

@router4.post("/vote_on_post",status_code=status.HTTP_201_CREATED)
def voting(vote : schema.setVote, db:Session = Depends(get_db),current_user: models.Users = Depends(oauth2.get_current_user)):
    """
        Cast or remove a vote on a post.

        This endpoint allows an authenticated user to upvote (dir=1) or remove their vote (dir≠1)
        from a specific post. Duplicate votes are not allowed. Only one vote per user per post is permitted.

        Args:
            vote: Contains post_id and direction (1 for upvote, 0 or other for removal).
            db: The database session.
            current_user: The currently authenticated user.

        Returns:
            A success message if the vote is added or removed.

        Raises:
            HTTPException:
                - 204: If the post does not exist.
                - 409: If the user has already voted on the post.
                - 404: If the user tries to remove a vote that does not exist.
        """
    post  = db.query(models.Post).filter(models.Post.id ==vote.user_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="post doesnot exist")
    owner = db.query(models.Users).filter(models.Users.email == current_user.id).first()
    v = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == owner.id).first()

    if(vote.dir == 1):
        if v:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on this post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id ,dir= vote.dir, user_id = owner.id)
        db.add(new_vote)
        db.commit()
        return {"msg" : "vote added successfully"}
    else:
        if not v:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        v.delete(synchronize_session = False)
        db.commit()
        return {"msg": "Sucessfully deleted message"}

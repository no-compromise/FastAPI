from multiprocessing import synchronize
from .. import models, schemas, utils, oath2, database
from fastapi import APIRouter, FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote")


@router.post("", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    curent_user: int = Depends(oath2.get_current_user),
):

    vote_q = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == curent_user.id,
    )
    vote_check_q = vote_q.first()

    if vote.dir == 1:

        if vote_check_q:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot vote twice on same post",
            )
        check_post_exist = (
            db.query(models.Post).filter(models.Post.id == vote.post_id).first()
        )
        if not check_post_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot vote on non existing post",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=curent_user.id)
        db.add(new_vote)
        db.commit()
        return {"data": "All OK, vote send"}

    else:
        if not vote_check_q:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        vote_q.delete(synchronize_session=False)
        db.commit()
        return {"data": "All OK, vote deleted"}

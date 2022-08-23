from .. import models, schemas, oath2
from fastapi import FastAPI, status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List

router = APIRouter(prefix="/posts")


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def post_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    user_id: int = Depends(oath2.get_current_user),
):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def pos_del(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    post.delete(synchronize_session=False)
    db.commit()


# comment


@router.put("/{id}")
def update_post(id: int, u_post: schemas.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    post_query.update(u_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": "Update OK!"}

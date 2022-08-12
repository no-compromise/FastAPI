# Only for testing

from typing import Optional
from fastapi.exceptions import HTTPException
from turtle import pos
from fastapi import FastAPI, status, Depends
from pydantic import BaseModel
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def get_root():
    return {"data": "root page"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_posts_id(id: int):
    # post = cursor.execute("""SELECT * FROM posts WHERE id = %s""", [id]).fetchone()
    # if not post:
    #    raise HTTPException(
    #        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found..."
    #    )
    return {"data": "post"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post):

    return {"data": "post"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def pos_del(id: int):
    pass

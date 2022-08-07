# Only for testing

from turtle import pos
from fastapi import FastAPI, status
import psycopg
from pydantic import BaseModel
from psycopg.rows import dict_row

try:
    conn = psycopg.connect(
        host="localhost",
        dbname="rapidapi",
        user="postgres",
        password="",
        row_factory=dict_row,
    )
    cursor = conn.cursor(row_factory=dict_row)
    print("Connection to DB OK!")
except Exception as error:
    print(error)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def get_root():
    return {"data": "root page"}


@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    # print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_posts(post: Post):
    post = cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    ).fetchone()
    conn.commit()
    return {"data": post}

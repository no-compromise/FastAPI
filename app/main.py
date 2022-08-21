from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def get_root():
    return {"data": "root page"}

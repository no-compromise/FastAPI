from email.policy import HTTP
from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", status_code=status.HTTP_404_NOT_FOUND)
def get_root():
    return {}

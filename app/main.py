from email.policy import HTTP
from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# -- Not anymore needed because of Alembic implementation
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["http://localhost", "http://localhost:8080", "https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/", status_code=status.HTTP_404_NOT_FOUND)
def get_root():
    return {}

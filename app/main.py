from email.policy import HTTP
from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import websocket

# -- Not anymore needed because of Alembic implementation
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

############ WS fetching

# -- Here must pass right arguments, and pass it for the first seconds!!!!!
pokecwss = "<url>"


async def read_websocket_pokec():
    # websocket.enableTrace(True)
    ws = websocket.WebSocket()
    ws.connect(pokecwss)
    ws.send('42["enterRoom",{"idRoom":9},null]')  # First send command to enter a room
    while True:
        # Read operation here, preferably in an async way
        print("--------------Reading...")
        msg = ws.recv()
        print(msg)
        print("--------------Going to sleep...")
        await asyncio.sleep(5)
        ws.ping()
        print("----------Ping sent")


############


@app.on_event("startup")
async def startup():
    asyncio.create_task(read_websocket_pokec())


origins = ["http://localhost", "http://localhost:8080"]

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


@app.get("/", status_code=status.HTTP_200_OK)
def get_root():
    pass

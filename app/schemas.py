from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
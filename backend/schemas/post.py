from pydantic import BaseModel
import schemas

class PostBase(BaseModel):
    title: str
    post_text: str

class PostUpdate(PostBase):
    pass

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    creator_id: int
    likes: list[schemas.Like]
    dislikes: list[schemas.Dislike]

    class Config:
        orm_mode = True
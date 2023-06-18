from datetime import datetime

from pydantic import BaseModel, EmailStr

# Use pydantic.BaseModel to specify what data structure and type we expect (schema declaration)


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    create_at: datetime  # this needs to be created_at

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True


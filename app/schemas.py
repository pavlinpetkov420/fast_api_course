from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field
from pydantic.dataclasses import ConfigDict


# Use pydantic.BaseModel to specify what data structure and type we expect (schema declaration)


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime  # this needs to be created_at
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponseVote(BaseModel):
    Post: PostResponse
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]


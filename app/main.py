from typing import Optional, Union

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app: FastAPI = FastAPI()


class Post(BaseModel):
    # Use pydantic.BaseModel to specify what data structure and type we expect (schema declaration)
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

try:
    connection = psycopg2.connect(host='localhost', database='fast_api', user='postgres',
                                    password='J0Gj_cLZTaCH0FqweV^O1A', cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database connection was successful!")
except Exception as ex:
    raise Exception(ex)


my_posts: list = [{'title': 'Top beaches in Florida', 'content': 'Checkout those top beaches in Florida!', 'published': True, 'rating': 2, 'id': 314}
                  , {'title': 'old_title', 'content': 'Content', 'published': True, 'rating': 3, 'id': 315}]


def filter_post_by_id(post_id: int):
    for post in my_posts:
        if post['id'] == post_id:
            return post


def find_post(post_id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == post_id:
            return i

"""
@app decorator - tells FastAPI that the function right below is in charge of handling requests that go to: 
    - the path /
    - using a get operation

Start the App Server: uvicorn main:app [--reload - this flag is used when you save the changes to see the immediately] 
"""


@app.get("/")
def root():
    return {"message": "Welcome to myAPI!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/id={post_id}")
def get_post(post_id: int):
    post: Union[dict, None] = filter_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    return {"post": post}


@app.delete("/posts/id={post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    index: Union[int, None] = find_post(post_id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/id={post_id}")
def update_post(post_id: int, post: Post):
    index: int = find_post(post_id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    post_dict: dict = post.dict()
    post_dict['id'] = post_id
    my_posts[index] = post_dict
    return {"data": post_dict}



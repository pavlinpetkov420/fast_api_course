from typing import Optional, Union

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

import sql.queries as queries
from .models import Base, Posts
from .database import engine, get_db


Base.metadata.create_all(bind=engine)

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
    # Format table and columns
    formatted_query: str = queries.INSERT_INTO_RETURNING_STAR.format(table="posts", column_names="title, content, published")
    # Execute insert statement
    cursor.execute(formatted_query, (post.title, post.content, post.published))
    connection.commit()
    # Return data
    new_post = cursor.fetchone()
    return {"data": new_post}


@app.get("/posts/id={post_id}")
def get_post(post_id: int):
    formatted_query: str = queries.FILTER_POST_BY_ID.format(table="fast_api.public.posts")
    cursor.execute(formatted_query, (str(post_id)))
    post = cursor.fetchall()
    # post: Union[dict, None] = filter_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    return {"post": post}


@app.delete("/posts/id={post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    formatted_query: str = queries.DELETE_POST_BY_ID.format(table="fast_api.public.posts")
    cursor.execute(formatted_query, (str(post_id)))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/id={post_id}")
def update_post(post_id: int, post: Post):
    formatted_query: str = queries.UPDATE_POST_BY_ID.format(table="fast_api.public.posts", column="id")
    cursor.execute(formatted_query, (post.title, post.content, post.published, str(post_id)))

    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")

    return {"data": updated_post}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()
    return {"status": "success",
            "data": posts}
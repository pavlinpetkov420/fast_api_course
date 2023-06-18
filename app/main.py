import datetime
from typing import Optional, Union, List

import sqlalchemy.exc
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

import sql.queries as queries
import app.models as models
from .database import engine, get_db
from app.schemas import PostResponse, CreatePost, UserCreate, UserResponse
from .utils import hash_pwd


models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()


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


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Posts).all()
    return all_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    # # Format table and columns
    # formatted_query: str = queries.INSERT_INTO_RETURNING_STAR.format(table="posts", column_names="title, content, published")
    # # Execute insert statement
    # cursor.execute(formatted_query, (post.title, post.content, post.published))
    # connection.commit()
    # new_post = cursor.fetchone()

    # Same functionality with ORM
    new_post = models.Posts(**post.__dict__)
    # Add the new post to table
    db.add(new_post)
    db.commit()
    # Retrieve same records, with default constraint values
    db.refresh(new_post)
    # Return data
    return new_post


@app.get("/posts/id={post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # formatted_query: str = queries.FILTER_POST_BY_ID.format(table="fast_api.public.posts")
    # cursor.execute(formatted_query, (str(post_id)))
    # post = cursor.fetchall()
    # post: Union[dict, None] = filter_post_by_id(post_id)

    # Do the same with ORM
    filtered_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()

    if not filtered_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    return filtered_post


@app.delete("/posts/id={post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # formatted_query: str = queries.DELETE_POST_BY_ID.format(table="fast_api.public.posts")
    # cursor.execute(formatted_query, (str(post_id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    # delete operation with ORM
    deleted_post = db.query(models.Posts).filter(models.Posts.id == post_id)

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/id={post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    # formatted_query: str = queries.UPDATE_POST_BY_ID.format(table="fast_api.public.posts", column="id")
    # cursor.execute(formatted_query, (post.title, post.content, post.published, str(post_id)))
    #
    # updated_post = cursor.fetchone()
    # connection.commit()
    #UPDATE post with ORM

    filtered_post = db.query(models.Posts).filter(models.Posts.id == post_id)

    if filtered_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")
    # Returns updated records count
    filtered_post.update(updated_post.__dict__, synchronize_session=False)
    db.commit()

    return filtered_post.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = hash_pwd(user.password)
        new_user = models.User(**user.__dict__)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f"There is existing user with e-mail address: {user.email}")

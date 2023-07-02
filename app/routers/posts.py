from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import PostResponse, CreatePost
from app.oauth2 import get_current_user


router = APIRouter(
    prefix='/posts'
    , tags=['Posts']
)


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


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    all_posts = db.query(models.Posts).all()
    return all_posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
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


@router.get("/id={post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
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


@router.delete("/id={post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
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
    return Response(status_code=status.HTTP_204_NO_CONTENT, description=f'Post with id {post_id} has been deleted!')


@router.put("/id={post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
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


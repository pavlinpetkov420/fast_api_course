from typing import List, Optional

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.openapi.models import Response
from sqlalchemy import func
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import PostResponse, CreatePost, UserResponse, PostResponseVote
from app.oauth2 import get_current_user


router = APIRouter(
    prefix='/posts'
    , tags=['Posts']
)

"""
@app decorator - tells FastAPI that the function right below is in charge of handling requests that go to: 
    - the path /
    - using a get operation

Start the App Server: uvicorn main:app [--reload - this flag is used when you save the changes to see the immediately] 
"""


# @router.get("/", response_model=List[PostResponse])
# @router.get("/")
@router.get("/", response_model=None)
def get_posts(
        db: Session = Depends(get_db),
        user: UserResponse = Depends(get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ''
) -> List[PostResponseVote]:
    """
        db: Session = connected session
        user: UserResponse = current user
        limit: int = limit how many posts to return, default = 10
        skip: int = skip first X posts, default = 0
        search: Optional[str] = Add keywords to filter posts

        Note for Postman: space between keywords for search is %20
    """
    # all_posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    # return all_posts

    votes_result = db.query(models.Posts, func.count(models.Votes.post_id).label("Votes"))\
        .join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True)\
        .group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    votes_result = list(map(lambda x: x._mapping, votes_result))
    return votes_result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db), user: UserResponse = Depends(get_current_user)):
    # # Format table and columns
    # formatted_query: str = queries.INSERT_INTO_RETURNING_STAR.format(table="posts", column_names="title, content, published")
    # # Execute insert statement
    # cursor.execute(formatted_query, (post.title, post.content, post.published))
    # connection.commit()
    # new_post = cursor.fetchone()

    # Same functionality with ORM
    new_post = models.Posts(owner_id=user.id, **post.__dict__)
    # Add the new post to table
    db.add(new_post)
    db.commit()
    # Retrieve same records, with default constraint values
    db.refresh(new_post)
    # Return data
    return new_post


@router.get("/id={post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), user: UserResponse = Depends(get_current_user)):
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
def delete_post(post_id: int, db: Session = Depends(get_db), user: UserResponse = Depends(get_current_user)):
    # formatted_query: str = queries.DELETE_POST_BY_ID.format(table="fast_api.public.posts")
    # cursor.execute(formatted_query, (str(post_id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    # delete operation with ORM
    filtered_post_query = db.query(models.Posts).filter(models.Posts.id == post_id)
    post = filtered_post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")

    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action!")

    filtered_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, description=f'Post with id {post_id} has been deleted!')


@router.put("/id={post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: CreatePost, db: Session = Depends(get_db),
                user: UserResponse = Depends(get_current_user)):
    # formatted_query: str = queries.UPDATE_POST_BY_ID.format(table="fast_api.public.posts", column="id")
    # cursor.execute(formatted_query, (post.title, post.content, post.published, str(post_id)))
    #
    # updated_post = cursor.fetchone()
    # connection.commit()
    #UPDATE post with ORM

    filtered_post_query = db.query(models.Posts).filter(models.Posts.id == post_id)
    post = filtered_post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no post with id {post_id}! Please provide other id!")

    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action!")

    # Returns updated records count
    filtered_post_query.update(updated_post.__dict__, synchronize_session=False)
    db.commit()

    return filtered_post_query.first()


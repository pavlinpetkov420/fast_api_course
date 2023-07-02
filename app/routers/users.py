import sqlalchemy.exc
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import app.models as models
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.utils import hash_pwd


router = APIRouter(
    prefix='/users'
    , tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
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


@router.get("/id={id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} doesn't exist." )

    return user

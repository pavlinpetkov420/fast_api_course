from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.utils import verify
from app.oauth2 import create_access_token

router: APIRouter = APIRouter(tags=['authentication'])


@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2PasswordRequestForm = {"username":"name", "password":"pwd"}
    """
    user_response = db.query(User).filter(User.email == user_credentials.username).first()

    if not user_response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials!')

    if not verify(user_credentials.password, user_response.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials!')

    # Create token
    access_token = create_access_token({"user_id": user_response.id, "user_email": user_response.email})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}







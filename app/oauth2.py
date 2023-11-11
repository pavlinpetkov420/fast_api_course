from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import TokenData
from app.database import get_db
from app.config import settings

# tokenUrl = router path for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret_key - verify data integrity of our token and resides on the server only
# algorithm - hs256
# expiration_time - 60min
SECRET_KEY: str = settings.secret_key
ALGORITHM: str = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode: dict = data.copy()
    # Prepare expiration time
    expiration_time: datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add to encode data dictionary
    to_encode.update({"exp": expiration_time})

    encoded_data = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_data


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could NOT validate creadentials!",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credentials_exception)

    current_user = db.query(User).filter(User.id == token.id).first()

    return current_user

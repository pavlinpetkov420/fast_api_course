from passlib.context import CryptContext

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str):
    """
    Hashing passwords which are stored in Database using bcrypt
    :return: !str
    """
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    """
    Verify plain and hashed password to authenticate a user to the system.
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)

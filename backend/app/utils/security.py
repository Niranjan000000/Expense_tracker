from datetime import datetime, timedelta, timezone

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.database.models import User
from dotenv import load_dotenv
import os

load_dotenv()


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth_2_scheme = HTTPBearer()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30



def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    print("PASSWORD:", password)
    print("PASSWORD LENGTH:", len(password))
    return pwd_context.hash(password)



def authenticate_user(db,email:str,password:str):
    user=db.query(User).filter(User.email==email).first()

    if not user:
        return False

    if not verify_password(
        password,
        user.password_hash
    ):
        return False

    return user

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def get_current_user(db, token: str):

    credentials_exception = Exception(
        "Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):

        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_id ).first()

    if user is None:
        raise credentials_exception

    return user


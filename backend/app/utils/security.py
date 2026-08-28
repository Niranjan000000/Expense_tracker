from datetime import datetime, timedelta, timezone


from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from app.database.models import User
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

oauth_2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

load_dotenv()


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth_2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


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

    print("TOKEN TYPE:", type(token))
    print("TOKEN RECEIVED:", bool(token))

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD:", payload)

    except Exception as e:

        print("JWT DECODE ERROR:", repr(e))
        raise e

    user_id = payload.get("sub")

    print("SUB:", user_id)

    if user_id is None:
        raise Exception("SUB is missing")

    user_id = int(user_id)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    print("USER:", user)

    if user is None:
        raise Exception("User not found")

    return user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User

from app.schemas.user import UserCreate,userresponse
from app.schemas.auth import Loginrequest, Token
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.security import (
    get_password_hash,
    authenticate_user,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=userresponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(
        user_data.password
    )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
        account_status=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=Token
)
def login(
    login_data: Loginrequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        login_data.email,
        login_data.password
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if user.account_status != True:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post(
    "/token",
    response_model=Token
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.account_status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


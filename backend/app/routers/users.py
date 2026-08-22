from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.user import userresponse,UserCreate
from fastapi.security import HTTPAuthorizationCredentials

from app.utils.security import (
    oauth_2_scheme,
    get_current_user
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=userresponse)
def get_my_profile(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials

        user = get_current_user(
            db,
            token
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user
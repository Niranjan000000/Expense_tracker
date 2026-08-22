from fastapi import FastAPI
from sqlalchemy import text
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router



app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


from fastapi import FastAPI
from sqlalchemy import text
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.expense import router as expense_router
from app.routers.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








app.include_router(auth_router)
app.include_router(users_router)
app.include_router(expense_router)
app.include_router(ai_router)

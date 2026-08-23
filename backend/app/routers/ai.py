from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Expense
from app.schemas.ai import AIAnalysisResponse
from app.utils.security import (
    get_current_user,
    oauth_2_scheme
)

from app.ai.service import analyze_expenses


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/analyze",
    response_model=AIAnalysisResponse
)
def analyze_user_expenses(
    credentials: HTTPAuthorizationCredentials = Depends(
        oauth_2_scheme
    ),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        db,
        token
    )

    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

    if not expenses:
        return {
            "analysis": "You don't have any expenses yet."
        }

    expense_data = "\n".join(
        [
            f"Amount: ₹{expense.amount}, "
            f"Category: {expense.category}, "
            f"Description: {expense.description}, "
            f"Date: {expense.expense_date}"
            for expense in expenses
        ]
    )

    analysis = analyze_expenses(
        expense_data
    )

    return {
        "analysis": analysis
    }
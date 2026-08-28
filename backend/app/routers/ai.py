from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict
from app.database.connection import get_db
from app.database.models import Expense
from app.schemas.ai import (AIAnalysisResponse,AnomalyResponse)
from app.utils.security import (
     oauth_2_scheme,
    get_current_user
)

from app.ai.service import (analyze_anomalies)

from app.ai.service import (analyze_expenses)


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/analyze",
    response_model=AIAnalysisResponse
)
def analyze_user_expenses(
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

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

    analysis = analyze_expenses(expense_data)

    return {
        "analysis": analysis
    }
@router.post(
    "/anomalies",
    response_model=AnomalyResponse
)
def detect_anomalies(
   token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):
    
    current_user = get_current_user(
        db,
        token
    )

    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

    if not expenses:
        return {
            "anomalies": []
        }

   

    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for expense in expenses:

        category_totals[
            expense.category
        ] += float(expense.amount)

        category_counts[
            expense.category
        ] += 1

    category_averages = {}

    for category in category_totals:

        category_averages[category] = (
            category_totals[category]
            / category_counts[category]
        )

   
    suspicious_expenses = []

    for expense in expenses:

        average = category_averages[
            expense.category
        ]

        amount = float(expense.amount)

        

        if amount >= average * 2.5:

            suspicious_expenses.append({
                "id": expense.id,
                "category": expense.category,
                "amount": amount,
                "description": expense.description,
                "date": str(expense.expense_date),
                "average": round(average, 2)
            })

    

    if not suspicious_expenses:

        return {
            "anomalies": []
        }

   
    anomaly_data = "\n".join(
        [
            f"""
Expense ID: {expense['id']}
Category: {expense['category']}
Amount: ₹{expense['amount']}
Description: {expense['description']}
Date: {expense['date']}
Category average: ₹{expense['average']}
"""
            for expense in suspicious_expenses
        ]
    )

    ai_analysis = analyze_anomalies(
        anomaly_data
    )

   
    anomalies = []

    for expense in suspicious_expenses:

        anomalies.append({
            "expense_id": expense["id"],
            "category": expense["category"],
            "amount": expense["amount"],
            "message": ai_analysis
        })

    return {
        "anomalies": anomalies
    }
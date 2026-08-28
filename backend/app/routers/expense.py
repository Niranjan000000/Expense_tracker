from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from datetime import date

from app.database.connection import get_db
from app.database.models import Expense

from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate
)

from app.schemas.summary import (
    ExpenseSummary,
    CategorySummary,
    MonthlySummary
)

from app.utils.security import (
    get_current_user,
    oauth_2_scheme
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)



@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(
    expense_data: ExpenseCreate,
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    new_expense = Expense(
        user_id=current_user.id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        expense_date=expense_data.expense_date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense




@router.get(
    "",
    response_model=list[ExpenseResponse]
)
def get_expenses(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    min_amount: Decimal | None = Query(default=None),
    max_amount: Decimal | None = Query(default=None),

    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    query = db.query(Expense).filter(
        Expense.user_id == current_user.id
    )

    # Category filter
    if category:
        query = query.filter(
            Expense.category == category
        )

    # Description search
    if search:
        query = query.filter(
            Expense.description.ilike(
                f"%{search}%"
            )
        )

    # Start date
    if start_date:
        query = query.filter(
            Expense.expense_date >= start_date
        )

    # End date
    if end_date:
        query = query.filter(
            Expense.expense_date <= end_date
        )

    # Minimum amount
    if min_amount is not None:
        query = query.filter(
            Expense.amount >= min_amount
        )

    # Maximum amount
    if max_amount is not None:
        query = query.filter(
            Expense.amount <= max_amount
        )

    expenses = query.all()

    return expenses



@router.get(
    "/summary",
    response_model=ExpenseSummary
)
def get_expense_summary(
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    total_expenses = db.query(
        func.count(Expense.id)
    ).filter(
        Expense.user_id == current_user.id
    ).scalar()

    total_amount = db.query(
        func.coalesce(
            func.sum(Expense.amount),
            0
        )
    ).filter(
        Expense.user_id == current_user.id
    ).scalar()

    return {
        "total_expenses": total_expenses,
        "total_amount": total_amount
    }




@router.get(
    "/summary/category",
    response_model=list[CategorySummary]
)
def get_category_summary(
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    results = db.query(
        Expense.category,
        func.sum(
            Expense.amount
        ).label("total")
    ).filter(
        Expense.user_id == current_user.id
    ).group_by(
        Expense.category
    ).all()

    return [
        {
            "category": category,
            "total": total
        }
        for category, total in results
    ]




@router.get(
    "/summary/monthly",
    response_model=list[MonthlySummary]
)
def get_monthly_summary(
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    results = db.query(
        func.date_format(
            Expense.expense_date,
            "%Y-%m"
        ).label("month"),

        func.sum(
            Expense.amount
        ).label("total")

    ).filter(
        Expense.user_id == current_user.id
    ).group_by(
        func.date_format(
            Expense.expense_date,
            "%Y-%m"
        )
    ).order_by(
        func.date_format(
            Expense.expense_date,
            "%Y-%m"
        )
    ).all()

    return [
        {
            "month": month,
            "total": total
        }
        for month, total in results
    ]



@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: int,
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense



@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    if expense_data.amount is not None:
        expense.amount = expense_data.amount

    if expense_data.category is not None:
        expense.category = expense_data.category

    if expense_data.description is not None:
        expense.description = expense_data.description

    if expense_data.expense_date is not None:
        expense.expense_date = expense_data.expense_date

    db.commit()
    db.refresh(expense)

    return expense



@router.delete(
    "/{expense_id}"
)
def delete_expense(
    expense_id: int,
    token: str = Depends(oauth_2_scheme),
    db: Session = Depends(get_db)
):

    current_user = get_current_user(
        db,
        token
    )

    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }
from fastapi import APIRouter, Depends, HTTPException, status,Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date
from app.database.connection import get_db
from app.database.models import Expense
from app.schemas.expense import (ExpenseCreate,ExpenseResponse,ExpenseUpdate)
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

    # Start with only current user's expenses
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
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: int,
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



@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(
    expense_id: int,
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
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: Decimal
    category: str
    description: str | None = None
    expense_date: date


class ExpenseUpdate(BaseModel):
    amount: Decimal | None = None
    category: str | None = None
    description: str | None = None
    expense_date: date | None = None


class ExpenseResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    description: str | None
    expense_date: date
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
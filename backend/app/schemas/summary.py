from decimal import Decimal

from pydantic import BaseModel


class ExpenseSummary(BaseModel):
    total_expenses: int
    total_amount: Decimal


class CategorySummary(BaseModel):
    category: str
    total: Decimal

class MonthlySummary(BaseModel):
    month: str
    total: Decimal

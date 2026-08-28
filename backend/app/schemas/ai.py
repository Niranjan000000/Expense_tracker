from pydantic import BaseModel


class AIAnalysisResponse(BaseModel):
    analysis: str


class AnomalyItem(BaseModel):
    expense_id: int
    category: str
    amount: float
    message: str


class AnomalyResponse(BaseModel):
    anomalies: list[AnomalyItem]
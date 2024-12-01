from pydantic import BaseModel

class User(BaseModel):
  income: float
  outcome: float
  saving_ratio: float
  financial_goals: str
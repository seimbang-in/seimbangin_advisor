from pydantic import BaseModel

class User(BaseModel):
  monthly_income: float
  outcome: float
  current_savings: float
  debt:float
  financial_goals: str
  risk_management: str
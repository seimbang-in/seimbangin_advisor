from pydantic import BaseModel

class Text(BaseModel):
  text:str

class PredictionResponse(BaseModel):
  text: str
  predicted_category: str
  confidence: float

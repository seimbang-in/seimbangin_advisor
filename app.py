from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import uvicorn
from utils.generate import get_financial_advice
from utils.model import load_model_forecasting
from utils.market import predict_market,define_market_condition
from models.User import User

app = FastAPI(
    title="Seimbangin financial advisor API",
    description="API for forecasting Indonesian market conditions and providing market analysis and give financial personal recommendations to users",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataset = pd.read_csv('./combined_dataset.csv')

@app.post("/get_advice")
async def get_advice(request: User):
    models = load_model_forecasting()
    predictions = predict_market(models,dataset,12)
    conditions = define_market_condition(predictions,dataset)
    context = f"""
    Income: Rp.{request.monthly_income}
    Outcome: Rp.{request.outcome}
    debt: Rp.{request.debt}
    current savings: Rp.{request.current_savings}
    rsik management: {request.risk_management}
    Financial Goals: {request.financial_goals}
    Market Conditions: {conditions}
    
    Based on financial situation above, give me a personalized financial advice.
    """
    response = get_financial_advice(context)
    return response

@app.post("/get_market_conditions")
async def get_market_conditions(month: int):
    models = load_model_forecasting()
    predictions = predict_market(models,dataset,month)
    conditions = define_market_condition(predictions,dataset)
    return conditions

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

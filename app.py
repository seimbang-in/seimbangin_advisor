from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import pandas as pd
import uvicorn
import numpy as np
from utils.generate import get_financial_advice
from utils.model import load_model_forecasting,load_model_text_classification,vectorize_text,predict_category
from utils.market import predict_market,define_market_condition
from models.User import User
from models.Text import Text,PredictionResponse
import json

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
    outcome: Rp.{request.outcome}
    debt: Rp.{request.debt}
    current savings: Rp.{request.current_savings}
    risk management: {request.risk_management}
    financial Goals: {request.financial_goals}
    market Conditions: {conditions}
    
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

@app.post("/text/classify")
async def classify_text(request:Text,response_model=PredictionResponse):
    MAX_LEN = 10
    model = tf.keras.models.load_model('./utils/klasifikasi.h5')
    with open('./utils/tokenizer.json','r') as f:
        tokenizer_json = json.load(f)
    tokenizer_string = json.dumps(tokenizer_json)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_string)
    category = {0 : 'transportation',
 1 : 'Food & Beverage',
 2 : 'healthy',
 3 : 'entertainment',
 4 : 'utility',
 5 : 'education',
 6 : 'shopping'}
    sequence = tokenizer.texts_to_sequences([request.text])
    padded_sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence,maxlen=MAX_LEN,padding='post')
    prediction = model.predict(padded_sequence)
    predict_category_id = np.argmax(prediction)
    category_mapping = category.get(predict_category_id,'Unknown')
    return PredictionResponse(text=request.text,predicted_category=category_mapping,confidence=float(np.max(prediction)))

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

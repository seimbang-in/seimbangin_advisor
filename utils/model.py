import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np
import pandas as pd
import os
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def load_model_forecasting():
    models = {}
    indicators = ['Rupiah']
    for indicator in indicators:
        models[indicator] = tf.keras.models.load_model(f"model_fix/{indicator}_model.h5")
    return models

def load_model_advisor():
    model = AutoModelForCausalLM.from_pretrained(
        "./Llama-3.2-1B-personal-finance",
        torch_dtype=torch.float16,  
        device_map="auto",
        low_cpu_mem_usage=True,
        offload_folder="offload" ,
        rope_scaling={"type": "linear", "factor": 32.0} ,
        ignore_mismatched_sizes=True
    ).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    

    model.eval()  
    if torch.cuda.is_available():
        model = model.cuda()
        torch.backends.cudnn.benchmark = True 
    
    tokenizer = AutoTokenizer.from_pretrained(
        f"./Llama-3.2-1B-personal-finance",
        model_max_length=512 
    )

    return model, tokenizer

def load_model_text_classification():
    model = tf.keras.models.load_model('./model/klasifikasi.h5')
    with open('./model/tokenizer.json','r') as f:
        tokenizer_json = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)
    return model,tokenizer

def vectorize_text(dataset):
    vectorizer = tf.keras.layers.TextVectorization(max_tokens=10000, output_mode='int')
    data = pd.read_csv(dataset)
    vectorizer.adapt(data['text'].values)
    return vectorizer

def predict_category(text, model, vectorizer, category_map):
    vectorized_text = vectorizer(text)
    prediction = model.predict(tf.expand_dims(vectorized_text, 0))
    predicted_category_id = np.argmax(prediction)

    # Reverse lookup category name
    reverse_category_map = {v: k for k, v in category_map.items()}
    return reverse_category_map[predicted_category_id]


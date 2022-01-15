# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 23:14:25 2022

@author: Jaspreet Singh
"""
from fastapi import FastAPI
from aapl_model_class import Newz_Senti
from Clean import clean
import pickle

# Creating Objects
app = FastAPI()
pickle_rfc = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/RFC_Model_AAPL.pkl", "rb")
pickle_tfidf = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/TFIDF_AAPL.pkl", "rb")
RFC = pickle.load(pickle_rfc)
tfidf_vec = pickle.load(pickle_tfidf)    
     
# Creating Root Page
@app.get("/Welcome_AAPL")
async def index():
    return "Hello! We will check Newz Headline's sentimental impact on Apple INC. (AAPL) Share Value."

# Creating Prediction Page
@app.post('/Predict_NewzHeadline_Sentiment_for_AAPL')     
async def senti_pred(data:Newz_Senti):
    data = data.dict()
    Newz = str(data['Newz_Headline'])
    Clean_Newz = clean(Newz)
    prediction = RFC.predict(tfidf_vec.transform([Clean_Newz]))
    if prediction[0] == 0:
        output = "Negative Newz Headline for AAPL Share Value"
    else:
        output = "Positive Newz Headline for AAPL Share Value"
    return {"Prediction Output": output, "Newz_Headline": Newz, "Clean_Newz_Headline": Clean_Newz}

print("Done")
# uvicorn app_aapl:app --reload
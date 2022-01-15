# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 23:14:25 2022

@author: Jaspreet Singh
"""
from fastapi import FastAPI
from aapl_model_class import Newz_Senti
import pickle

# Creating Objects
app = FastAPI()
pickle_rfc = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/RFC_Model_AAPL.pkl", "rb")
pickle_tfidf = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/TFIDF_AAPL.pkl", "rb")
pickle_stop = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/stop_nltk.pkl", "rb")
pickle_exclude = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/exclude_nltk.pkl", "rb")
pickle_lemma = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/2. Apple_StockValue_Analysis_using_Newz/Deployment/lemma_nltk.pkl", "rb")
RFC = pickle.load(pickle_rfc)
tfidf_vec = pickle.load(pickle_tfidf)
stop = pickle.load(pickle_stop)
exclude = pickle.load(pickle_exclude)
lemma = pickle.load(pickle_lemma)

# Creating clean function Using NLTK.
# Removing stopwords, Punctuations and doing lemmatization
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

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

if __name__ == '__main__':
    uvicorn.run(app)
# uvicorn app_aapl:app --reload
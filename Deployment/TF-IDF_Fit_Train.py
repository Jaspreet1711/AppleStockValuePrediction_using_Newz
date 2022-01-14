# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 19:34:38 2022

@author: Jaspreet Singh
"""
import pandas as pd

#Reading in data and looking at the number of rows and columns using shape 
x_train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/x_train.csv')
y_train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/y_train.csv')

# Creating TF-IDF for Text using x_train
from sklearn.feature_extraction.text import TfidfVectorizer

# Converting the x_train and x_test dataframe to list data structure. As TfidfVectorizer doesn't work with dataframe. 
Headlines_Train = x_train['Top_Headlines_words'].tolist()

# Setting up the parameters for TfidfVectorizer. It will be creating Unigrams, Bigrams and Trigrams
tfidf_vec = TfidfVectorizer(max_features = None, max_df = 0.8, min_df = 5, ngram_range = (1,3))

# Fitting the TfidfVectorizer on Train Data
tfidf_vec.fit(Headlines_Train)

# Transforming Train Fit TfidfVectorizer on x_train.
train_set = tfidf_vec.transform(Headlines_Train)

# converting the model into pickle
import pickle
file = open('TFIDF_AAPL.pkl', 'wb')
pickle.dump(tfidf_vec, file)
print("Done")
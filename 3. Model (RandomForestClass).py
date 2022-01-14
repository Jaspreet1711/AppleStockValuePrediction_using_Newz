# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:15:54 2022
@author: Jaspreet Singh
"""
import pandas as pd
import numpy as np

#Reading in data and looking at the number of rows and columns using shape 
x_train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/x_train.csv')
y_train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/y_train.csv')
x_test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/x_test.csv')
y_test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/3. TFIDF/y_test.csv')

# Creating TF-IDF for Text using x_train
from sklearn.feature_extraction.text import TfidfVectorizer

# Converting the x_train and x_test dataframe to list data structure. As TfidfVectorizer doesn't work with dataframe. 
Headlines_Train = x_train['Top_Headlines_words'].tolist()
Headlines_Test = x_test['Top_Headlines_words'].tolist()

# Setting up the parameters for TfidfVectorizer. It will be creating Unigrams, Bigrams and Trigrams
tfidf_vec = TfidfVectorizer(max_features = None, max_df = 0.8, min_df = 5, ngram_range = (1,3))

# Fitting the TfidfVectorizer on Train Data
tfidf_vec.fit(Headlines_Train)

# Transforming Train Fit TfidfVectorizer on on both and x_train and x_test Data.
train_set = tfidf_vec.transform(Headlines_Train)
test_set = tfidf_vec.transform(Headlines_Test)

# -- Model -- #
# Random Forest Classifier (RFC)
from sklearn.ensemble import RandomForestClassifier

# Setting up the Parameters for RFC after Hyperparameter Tuning.
RFC = RandomForestClassifier(n_estimators = 100, min_samples_split = 2, min_samples_leaf = 5, max_features = 'sqrt', max_depth = 10, random_state = 42)

# Fitting the RandomForest Regression model on Train Data.
RFC.fit(train_set, y_train['Pos/Neg_nextday_Change'])

# -- Model Evaluation -- #
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# -- Predicting results on Test Set for Evaluation
predictions_rfc = RFC.predict(test_set)

matrix = confusion_matrix(y_test, predictions_rfc)
print(matrix)
print(" ")

acc_score = accuracy_score(y_test, predictions_rfc)
print(np.round(acc_score, 2))
print(" ")

report = classification_report(y_test, predictions_rfc)
print(report)

# converting the model into pickle
import pickle
file = open('RFC_Model_AAPL.pkl', 'wb')
pickle.dump(RFC, file)


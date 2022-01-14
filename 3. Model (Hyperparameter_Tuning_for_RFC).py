import pandas as pd
import numpy as np


#Reading in data and looking at the number of rows and columns using shape 
x_train = pd.read_csv('x_train.csv')
y_train = pd.read_csv('y_train.csv')
x_test = pd.read_csv('x_test.csv')
y_test = pd.read_csv('y_test.csv')

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

## -- Performing Hyperparameter Tuning using Randomized Search CV -- ##

# Importing RandomizedSearchCV from sklearn.
from sklearn.model_selection import RandomizedSearchCV

#----------------------------------------------------------------------------#
# -- number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1500, num =15)]
# -- number of features to consider at every split 
max_features = ['auto', 'sqrt']
# -- maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# -- minimum number of samples required to split a node 
min_samples_split = [ 2, 5, 10, 15, 100]
# -- minimum number of samples required at each leaf node 
min_samples_leaf = [ 1, 2, 5, 10]
#----------------------------------------------------------------------------#
  
# Creating the Random Grid 
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}
print(random_grid)
print(" ")

# Importing RandomForest Regression
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier()

# Random Searching of parameters, using 3 folds cross validation.
# -- It will try 100 different combinations of paratmeters to determine the best score.
rf_random = RandomizedSearchCV(estimator = RFC, 
                               param_distributions = random_grid, 
                               scoring = 'neg_mean_squared_error', 
                               n_iter = 100, 
                               cv = 3, 
                               verbose = 2, 
                               random_state = 10)

# Fitting the train data and searching the best parameters to get high accuracy using Random Forest Classifier.
rf_random.fit(train_set, y_train['Pos/Neg_nextday_Change'])                               
print(" ")

# Getting the best parameters and accuracy score.
print(rf_random.best_params_)
print(" ")
print(rf_random.best_score_)
print(" ")





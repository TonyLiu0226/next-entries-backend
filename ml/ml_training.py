import os
from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sklearn
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

#loads data from a txt file
#file: file to read from. Each line in file must be split into two parts with a specified character char
#char: character to split each line with
#arr: array to store each line

def load_data(file, char, arr):
    with open(file) as f:
        for line in f:
            segments = line.split(char)
            list = []
            list.append(segments[0])
            list.append(segments[1].split('\n')[0])
            arr.append(list)
    return None

def train_logistic_regression(X_train, y_train, X_test, y_test):
    #performs 5-fold cross validation on the training set
    lr = LogisticRegression(penalty='l2', tol=0.0001, C=10, class_weight=None, 
                            random_state=123, solver='lbfgs', max_iter=10000, n_jobs=4)
    training_score = cross_validate(lr, X_train, y_train, cv=5, return_train_score=True)
    print(training_score)
    #using the best performing model, evaluate it on the testing set


#preprocesses data using sentence transformers
#data: the data to process
#df: the dataframe to reference (for indexing)
def preprocess_data(data, df):
    embedder = SentenceTransformer("paraphrase-distilroberta-base-v1")
    emb_sents = embedder.encode(data.tolist())
    preprocessed_df = pd.DataFrame(emb_sents, index=df.index)
    print(preprocessed_df)
    return preprocessed_df

#loading data
train_data = []
test_data = []
load_data("./emotions/train.txt", ';', train_data)
load_data("./emotions/val.txt", ';', train_data)
load_data("./emotions/test.txt", ";", test_data)

train_df = pd.DataFrame(data=train_data, columns=["entries", "emotions"])
test_df = pd.DataFrame(data=test_data, columns=["entries", "emotions"])

X_train = train_df.drop("emotions", axis=1)
X_test = test_df.drop("emotions", axis=1)
y_train = train_df["emotions"]
y_test = test_df["emotions"]

#preprocessing
X_train_transformed = preprocess_data(X_train['entries'], train_df)
X_test_transformed = preprocess_data(X_test['entries'], test_df)

#model training
train_logistic_regression(X_train_transformed, y_train, X_test_transformed, y_test)
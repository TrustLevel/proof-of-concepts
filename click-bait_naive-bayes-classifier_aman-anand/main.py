import numpy as np 
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string as s
import re

import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import os

# load dataset
cb_data= pd.read_csv('clickbait_data_sample.csv')
cb_data.head()

# split into train and test sets
x=cb_data.headline
y=cb_data.clickbait
train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.25,random_state=2)

# analyzing traind and test data
print("No. of elements in training set")
print(train_x.size)
print("No. of elements in testing set")
print(test_x.size)
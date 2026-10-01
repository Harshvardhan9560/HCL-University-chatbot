import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re
import nltk

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import joblib

df = pd.read_excel(r"E:\ml-HCL\dataset\AI-Powered Chatbot.xlsx")

print(df.head())
print(df.shape)
print(df.columns)

print(df.info())
print(df.isnull().sum())

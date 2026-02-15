import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import mean_absolute_error , r2_score
import joblib
df=pd.read_csv("dataset.csv")


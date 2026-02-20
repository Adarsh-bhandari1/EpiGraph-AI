import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from xgboost import  XGBRegressor
from sklearn.metrics import mean_absolute_error , r2_score
import joblib
df=pd.read_csv("dataset.csv")
# Sepreating the features and the target variable (infected_after_10)
X  = df.drop("infected_after_10" , axis=1)
y= df["infected_after_10"]
X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.2 , random_state=42)
#defining the model
model= XGBRegressor(n_estimators=300 , learning_rate=0.05 , max_depth=6 , random_state=42)

#training the model

model.fit(X_train , y_train , eval_set=[(X_test , y_test)] , early_stopping_rounds=20 , verbose=False)

predictions=model.predict(X_test)

mae=mean_absolute_error(y_test , predictions)
r2 = r2_score(y_test , predictions)
print("Model Evaluation Results")
print("-------------------------")
print("Mean Absolute Error:", round(mae, 2))
print("R² Score:", round(r2, 3))





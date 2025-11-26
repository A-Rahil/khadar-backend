import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from xgboost import XGBClassifier

features = [
    'Soil_Type',
    'Sunlight_Hours',
    'Water_Frequency',
    'Fertilizer_Type',
    'Temperature',
    'Humidity'
]

label = 'Growth_Milestone'   # 1 = ready to yield, 0 = not ready

df = pd.read_csv(r"plant_growth_data.csv")

categorical_cols = ['Soil_Type', 'Water_Frequency', 'Fertilizer_Type']
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le  # store encoder if you need for inference later

X, y = df[features], df[label].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

yieldModel = XGBClassifier(
    n_estimators=1500,
    max_depth=5,
    learning_rate=0.02,
    subsample=0.8,
    colsample_bytree=0.9,
    reg_lambda=1,
    n_jobs=-1,
    eval_metric="logloss",
    verbosity=0,
    device='cuda'
)

yieldModel.fit(X_train, y_train)

y_pred = yieldModel.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Yield Prediction Model Accuracy: {accuracy:.4f}")

with open('yieldModel.pkl', 'wb') as f:
    pickle.dump(yieldModel, f)
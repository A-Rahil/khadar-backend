import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import pickle
from xgboost import XGBClassifier

dataSet = pd.read_csv(r"Crop_recommendation.csv")
features = [
    'N',
    'P', 
    'K', 
    'temperature', 
    'humidity', 
    'ph', 
    'rainfall'
]

label = 'label'

X = dataSet[features]
y = dataSet[label]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

plantRecomm = XGBClassifier(
    n_estimators=2000,
    max_depth=6,
    learning_rate=0.01,
    reg_lambda=1,
    n_jobs=-1,  #using all cores of the cpu
    subsample=0.8,
    verbosity=0 #to avoid any outputs onto the console
)

plantRecomm.fit(X_train, y_train)
y_pred = plantRecomm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy is: {accuracy}")


with open('recommendation_model.pkl', 'wb') as f:
    pickle.dump(plantRecomm, f)

with open('recommend_X_test.pkl', 'wb') as f:
    pickle.dump(X_test, f)
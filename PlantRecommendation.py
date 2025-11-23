import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

dataPath = #need to define this later on Kaggle 
dataSet = pd.read_csv(dataPath)
features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = dataSet[features]
y = dataSet['label']

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

XGBclf = XGBClassifier(
    n_estimators=2000,
    max_depth=6,
    learning_rate=0.01,
    reg_lambda=1,
    n_jobs=-1,  #using all cores of the cpu
    subsample=0.8,
    verbosity=0 #to avoid any outputs onto the console
)

XGBclf.fit(X_train, y_train, eval_metric='auc', verbose=False)
score = cross_val_score(XGBclf, X, y_encoded, scoring='roc_auc_ovr', cv=5)  #taking the average
print("Model's Average ROC-AUC: ", score.mean())
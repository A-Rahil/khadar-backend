import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score


features = [
    'soil_moisture_%',  #Needs to be moderate, low leads to stress and high leads to fungi
    'soil_pH',  #Needs to be neutral
    'temperature_C',    #Needs to be moderate
    'rainfall_mm',
    'humidity_%',
    'sunlight_hours',
    'NDVI_index', #Normalized difference vegitation index, low leads to plant stress

    #Lesser so contributing factors to health predictions
    'pesticide_usage_ml',
    'fertilizer_type',
    'crop_type'
]

label = 'crop_disease_status'

df = pd.read_csv(r"C:\Users\ahmra\Downloads\Smart_Farming_Crop_Yield_2024.csv")

encoder_features = LabelEncoder()
df['crop_type'] = encoder_features.fit_transform(df['crop_type'])
df['fertilizer_type'] = encoder_features.fit_transform(df['fertilizer_type'])

encoder_label = LabelEncoder()
df['crop_disease_status'] = encoder_label.fit_transform(df['crop_disease_status'])
df['crop_disease_status'] = df['crop_disease_status'].apply(lambda x:0 if x==0 else 1)

X, y = df[features], df[label]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)

diseasePred = RandomForestClassifier(
    n_estimators=1000,
    max_depth=6,
    n_jobs=-1,
)

diseasePred.fit(X_train, y_train)
y_pred = diseasePred.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy is: {accuracy}")

print(df['crop_disease_status'].value_counts())
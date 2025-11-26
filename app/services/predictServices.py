import os
import pandas as pd
import pickle

baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
modelDir = os.path.join(baseDir, 'models')

try:
    diseaseModelPath = os.path.join(modelDir, 'diseaseModel.pkl')
    with open(diseaseModelPath, 'rb') as f:
        diseaseModel = pickle.load(f)
except FileNotFoundError:
    print("Disease model not found at ", diseaseModelPath)
    diseaseModel = None

try:
    recommendModelPath = os.path.join(modelDir, 'recommendation_model.pkl')
    with open(recommendModelPath, 'rb') as f:
        recommendModel = pickle.load(f)
except FileNotFoundError:
    print("Recommendation model not found at ", recommendModelPath)
    recommendModel = None

def getDiseasePred(data):
    if not diseaseModel:
        return None
    try:
        df = pd.DataFrame([data])
        prediction = diseaseModel.predict(df)
        return int(prediction[0])
    except Exception as e:
        print("Prediction error: ", e)
        return None

def getRecommend(data):
    if not recommendModel:
        return None
    try:
        df = pd.DataFrame([data])
        prediction = recommendModel.predict(df)
        return str(prediction[0])
    except Exception as e:
        print("Recommendation error: ", e)
        return None
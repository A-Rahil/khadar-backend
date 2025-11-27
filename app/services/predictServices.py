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
    
try:
    yieldModelPath = os.path.join(modelDir, 'yieldModel.pkl')
    with open(yieldModelPath, 'rb') as f:
        yieldModel = pickle.load(f)
except FileNotFoundError:
    print("Yield prediction model not found at ", yieldModelPath)
    yieldModel = None
    
try:
    recoLabelMapPath = os.path.join(modelDir, 'recommendation_label_mapping.pkl')
    with open(recoLabelMapPath, 'rb') as f:
        recoLabelMap = pickle.load(f)
except FileNotFoundError:
    print("Label mapping not found at ", recoLabelMapPath)
    recoLabelMap = None

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
    
def getYieldPred(data):
    if not yieldModel:
        return None
    try:
        df = pd.DataFrame([data])
        prediction = yieldModel.predict(df)
        return int(prediction[0])
    except Exception as e:
        print("Yield prediction error: ", e)
        return None
    
def getRecommend(data):
    if not recommendModel:
        return None
    try:
        df = pd.DataFrame([data])
        encoded_pred = recommendModel.predict(df)[0]

        # decode
        if recoLabelMap:
            decoded_label = recoLabelMap.get(int(encoded_pred), "Unknown")
        else:
            decoded_label = encoded_pred  # fallback
        return decoded_label
    
    except Exception as e:
        print("Recommendation error: ", e)
        return None

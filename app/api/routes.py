from flask import Flask, request, jsonify, Blueprint
from app.services.predictServices import getDiseasePred, getRecommend, getYieldPred
from app.dummy.dummyData import load_random_sample

routes = Blueprint("routes", __name__)

# predict_plant_health
@routes.route('/api/predict_plant_health', methods=['GET'])
def predict_plant_health():
    data = load_random_sample("disease_X_test.pkl")

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getDiseasePred(data)
        return jsonify({
            "model": "Random Forest",
            "result": result,
            "input_used": data   # optional - helps you debug
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# plant_recommendation
@routes.route('/api/plant_recommendation', methods=['GET'])
def plant_recommendation():
    data = load_random_sample("recommendation_X_test.pkl")

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getRecommend(data)
        return jsonify({
            "model": "XGBoost",
            "result": result,
            "input_used": datap
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# crop_yield
@routes.route('/api/crop_yield', methods=['GET'])
def crop_yield():
    data = load_random_sample("yield_X_test.pkl")

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getYieldPred(data)
        return jsonify({
            "model": "XGBoost",
            "result": result,
            "input_used": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
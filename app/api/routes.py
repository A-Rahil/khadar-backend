from flask import Flask, request, jsonify, Blueprint
from app.services.predictServices import getDiseasePred, getRecommend, getYieldPred
from app.dummy.dummyData import disease_data, recommendation_data, yield_data

routes = Blueprint("routes", __name__)

# predict_plant_health
@routes.route('/api/predict_plant_health', methods=['GET'])
def predict_plant_health():
    data = disease_data

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getDiseasePred(data)
        return jsonify({
            "model": "Random Forest",
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# plant_recommendation
@routes.route('/api/plant_recommendation', methods=['GET'])
def plant_recommendation():
    data = recommendation_data

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getRecommend(data)
        return jsonify({
            "model": "XGBoost",
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# crop_yield
@routes.route('/api/crop_yield', methods=['GET'])
def crop_yield():
    data = yield_data

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getYieldPred(data)
        return jsonify({
            "model": "XGBoost",
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
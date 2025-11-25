from flask import Flask, request, jsonify, Blueprint
from services.predictServices import getDiseasePred, getRecommend

routes = Blueprint("routes", __name__)

# predict_plant_health
@routes.route('/api/predict_plant_health', methods=['POST'])
def predict_plant_health():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        prediction = getDiseasePred(data)
        return jsonify({
            "model": "Random Forest",
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# plant_recommendation
@routes.route('/api/plant_recommendation', methods=['POST'])
def plant_recommendation():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getRecommend(data)
        return jsonify({
            "model": "XGBoost",
            "recommendation": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
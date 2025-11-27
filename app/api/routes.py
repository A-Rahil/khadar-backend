from flask import Flask, request, jsonify, Blueprint
from app.services.predictServices import getDiseasePred, getRecommend, getYieldPred
from app.dummy.dummyData import load_random_sample, new_load_random_samples

routes = Blueprint("routes", __name__)

@routes.route('/api/predict_plant_health', methods=['GET'])
def predict_plant_health():
    data_list = new_load_random_samples("disease_X_test.pkl", n=100)

    if not data_list:
        return jsonify({'error': 'No input received'}), 400

    try:
        results = []
        for data in data_list:
            pred = getDiseasePred(data)
            results.append({
                "input": data,
                "prediction": pred
            })

        return jsonify({
            "model": "Random Forest",
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# plant_recommendation
@routes.route('/api/plant_recommendation', methods=['GET'])
def plant_recommendation():
    data = load_random_sample("recommend_X_test.pkl")

    if not data:
        return jsonify({'error': 'No input received'}), 400
    
    try:
        result = getRecommend(data)
        return jsonify({
            "model": "XGBoost",
            "result": result,
            "input_used": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/crop_yield', methods=['GET'])
def crop_yield():
    data_list = new_load_random_samples("yield_X_test.pkl", n=100)

    if not data_list:
        return jsonify({'error': 'No input received'}), 400

    try:
        results = []
        for data in data_list:
            pred = getYieldPred(data)
            results.append({
                "input": data,
                "prediction": pred
            })

        return jsonify({
            "model": "XGBoost",
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
l
from unittest.mock import patch, MagicMock
import pytest

def test_getDiseasePred_and_getRecommend():
    # Create separate mocks for each model
    mock_disease_model = MagicMock()
    mock_disease_model.predict.return_value = [1]

    mock_recommend_model = MagicMock()
    mock_recommend_model.predict.return_value = ['rice']

    # Patch pickle.load for both calls
    with patch("pickle.load", side_effect=[mock_disease_model, mock_recommend_model]):
        import predictServices  # Import after patching

        # Disease prediction test
        disease_input = {
            'soil_moisture_%': 50,
            'soil_pH': 6.5,
            'temperature_C': 25,
            'rainfall_mm': 100,
            'humidity_%': 60,
            'sunlight_hours': 6,
            'NDVI_index': 0.7,
            'pesticide_usage_ml': 10,
            'fertilizer_type': 'A',
            'crop_type': 'cotton'
        }
        assert predictServices.getDiseasePred(disease_input) == 1

        # Recommendation test
        recommend_input = {
            'N': 10,
            'P': 5,
            'K': 1,
            'temperature': 25,
            'humidity': 60,
            'ph': 6.5,
            'rainfall': 100
        }
        assert predictServices.getRecommend(recommend_input) == 'rice'

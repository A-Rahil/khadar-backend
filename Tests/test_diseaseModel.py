import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_df():
    data = {
        'soil_moisture_%': [30, 40, 50, 60],
        'soil_pH': [6.5, 7.0, 6.8, 7.2],
        'temperature_C': [24, 26, 28, 25],
        'rainfall_mm': [100, 120, 80, 90],
        'humidity_%': [60, 65, 55, 70],
        'sunlight_hours': [6, 7, 8, 5],
        'NDVI_index': [0.6, 0.7, 0.5, 0.8],
        'pesticide_usage_ml': [10, 20, 15, 5],
        'fertilizer_type': ['A', 'B', 'A', 'C'],
        'crop_type': ['cotton', 'wheat', 'cotton', 'rice'],
        'crop_disease_status': ['healthy', 'diseased', 'healthy', 'diseased']
    }
    return pd.DataFrame(data)

@patch("pandas.read_csv")
@patch("xgboost.XGBClassifier")
@patch("pickle.dump")
@patch("sklearn.model_selection.train_test_split")
def test_disease_model_training(mock_split, mock_pickle, mock_xgb, mock_read_csv, mock_df):
    mock_read_csv.return_value = mock_df

    # Make train_test_split return arrays of the same length as predict
    X_train = mock_df.iloc[:2, :-1]
    X_test = mock_df.iloc[:2, :-1]
    y_train = [0, 1]
    y_test = [0, 1]
    mock_split.return_value = (X_train, X_test, y_train, y_test)

    # Mock XGBClassifier
    mock_model = MagicMock()
    mock_model.predict.return_value = [0, 1]  # must match length of y_test
    mock_xgb.return_value = mock_model

    # Import script
    import diseaseModel

    # Assertions
    mock_read_csv.assert_called_once()
    mock_split.assert_called_once()
    mock_model.fit.assert_called_once()
    mock_model.predict.assert_called_once()
    mock_pickle.assert_called_once()

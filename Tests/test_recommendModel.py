import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_dataset():
    data = {
        'N': [10, 20, 30, 40],
        'P': [5, 10, 15, 20],
        'K': [1, 2, 3, 4],
        'temperature': [25, 26, 22, 27],
        'humidity': [60, 65, 70, 65],
        'ph': [6.5, 7.0, 6.8, 7.1],
        'rainfall': [100, 120, 90, 110],
        'label': ['rice', 'wheat', 'rice', 'corn']
    }
    return pd.DataFrame(data)

# Patch read_csv, XGBClassifier, pickle, and train_test_split
@patch("pandas.read_csv")
@patch("xgboost.XGBClassifier")
@patch("pickle.dump")
@patch("sklearn.model_selection.train_test_split")
def test_recommend_model_training(mock_split, mock_pickle, mock_xgb, mock_read_csv, mock_dataset):
    mock_read_csv.return_value = mock_dataset

    # Patch train_test_split to return matching sizes
    X_train = mock_dataset.iloc[:2, :-1]
    X_test = mock_dataset.iloc[:2, :-1]
    y_train = [0, 1]
    y_test = [0, 1]
    mock_split.return_value = (X_train, X_test, y_train, y_test)

    # Mock XGBClassifier
    mock_model = MagicMock()
    mock_model.predict.return_value = [0, 1]  # same length as y_test
    mock_xgb.return_value = mock_model

    # Importing script now runs without crashing
    import recommendModel

    # Assertions
    mock_read_csv.assert_called_once()
    mock_split.assert_called_once()
    mock_model.fit.assert_called_once()
    mock_model.predict.assert_called_once()
    mock_pickle.assert_called_once()

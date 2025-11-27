import builtins
import pytest
from unittest.mock import patch, MagicMock, mock_open

@patch("pickle.dump")
@patch("sklearn.metrics.accuracy_score")   # <---- PATCH THIS
@patch("pandas.read_csv")
@patch("xgboost.XGBClassifier")
def test_yield_model_training(mock_xgb, mock_read_csv, mock_acc, mock_pickle_dump):
    # ----------- Fake CSV dataframe ----------------
    import pandas as pd
    fake_df = pd.DataFrame({
        "Soil_Type": ["A", "B", "A"],
        "Sunlight_Hours": [5, 6, 7],
        "Water_Frequency": ["Low", "High", "Low"],
        "Fertilizer_Type": ["X", "Y", "X"],
        "Temperature": [25, 26, 24],
        "Humidity": [60, 58, 65],
        "Growth_Milestone": [1, 0, 1],
    })
    mock_read_csv.return_value = fake_df

    mock_acc.return_value = 1.0  # prevent accuracy calculation crash

    # ----------- Fake XGB model ----------------
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]  # <---- length 1 to avoid mismatch
    mock_xgb.return_value = mock_model

    # Run module import (executes training code)
    import yieldModel

    # ----------- Tests ----------------

    mock_read_csv.assert_called_once_with("plant_growth_data.csv")

    assert "Soil_Type" in yieldModel.encoders
    assert "Water_Frequency" in yieldModel.encoders
    assert "Fertilizer_Type" in yieldModel.encoders

    mock_xgb.assert_called_once()
    kwargs = mock_xgb.call_args.kwargs

    assert kwargs["n_estimators"] == 1500
    assert kwargs["max_depth"] == 5
    assert kwargs["learning_rate"] == 0.02
    assert kwargs["device"] == "cuda"

    assert mock_model.fit.called
    assert mock_model.predict.called
    assert mock_pickle_dump.called

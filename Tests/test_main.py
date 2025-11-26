import pytest
from unittest.mock import patch, MagicMock


@patch("api.routes.routes")
def test_flask_app_loads(mock_routes):
    with patch("flask.Flask.register_blueprint") as mock_register:
        import main

        mock_register.assert_called_once_with(mock_routes)

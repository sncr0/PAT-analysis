import pytest
import numpy as np
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app

client = TestClient(app)


@pytest.fixture
def sample_payload():
    return {
        "model_name": "pls-acetone-acetonitrile",
        "payload": {
            "x": [0.1] * 14106  # Adjust length to match your PLS model input shape
        }
    }


@patch("backend.api.services.processing.inference_service.load_model")
def test_dispatch_processing_route(mock_load_model, sample_payload):
    # Mock the model and prediction behavior
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[0.42]])  # simulate prediction result
    mock_load_model.return_value = mock_model

    response = client.post("/process", json=sample_payload)

    if response.status_code != 200:
        print("❌ Error response:", response.status_code, response.json())

    assert response.status_code == 200
    assert "predicted_concentration" in response.json()
    assert response.json()["predicted_concentration"] == 0.42
    assert response.json()["message"] == "Processing dispatched successfully."

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from core.data_readers.infrared_reader import InfraredReader


client = TestClient(app)


@pytest.fixture
def spectrum_from_jdx():
    reader = InfraredReader()
    measurement = reader.read_file("data/acetonitrile-acetone/67-64-1-IR.jdx")
    return {
        "model_name": "pls-acetone-acetonitrile",
        "payload": {
            "x": measurement.data["y"].tolist()  # or .tolist() if needed
        }
    }


def test_real_prediction_from_api(spectrum_from_jdx):
    response = client.post("/process", json=spectrum_from_jdx)
    print("Response:", response.status_code, response.json())
    if response.status_code != 200:
        print("❌ Error response:", response.status_code, response.json())

    assert response.status_code == 200
    assert "predicted_concentration" in response.json()
    assert isinstance(response.json()["predicted_concentration"], float)

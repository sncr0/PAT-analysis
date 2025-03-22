import json
import requests
from src.data_formats.infrared_datapoint import InfraredDatapoint

# Dummy endpoint URL for the hypothetical cloud API.
CLOUD_API_URL = "http://localhost:8000/api/spectrum"


HEADERS = {
    "x-token": "secret-token"  # The API requires this exact token
}


def send_datapoint(datapoint: InfraredDatapoint):
    """
    Convert the InfraredDatapoint to a JSON payload and send it via an HTTP POST
    to a cloud API endpoint with authentication.
    """
    data_records = datapoint.data.to_dict(orient="records")
    time_str = str(datapoint.time) if datapoint.time is not None else "N/A"

    payload = {
        "timestamp": time_str,
        "data": data_records,
    }

    print("Sending JSON Payload:")
    # print(json.dumps(payload, indent=2))

    try:
        response = requests.post(CLOUD_API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        print("Successfully sent datapoint to cloud.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send datapoint: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Server Response:", e.response.text)

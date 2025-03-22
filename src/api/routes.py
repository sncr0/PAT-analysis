# src/api/routes.py

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from src.api.authentication import verify_token
from src.api.processing import process_spectrum, plot_latest_spectrum, upload_spectrum_to_db
from contextlib import asynccontextmanager
from src.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize the database
    init_db()
    yield
    # Shutdown: add any cleanup logic here if needed


app = FastAPI(lifespan=lifespan)


class SpectrumPayload(BaseModel):
    timestamp: str
    data: list[dict]


@app.post("/api/spectrum", dependencies=[Depends(verify_token)])
async def receive_spectrum(payload: SpectrumPayload):
    """
    Endpoint to receive spectroscopic payloads from edge devices.
    It processes the incoming data, uploads it to the database, and returns a status message.
    """
    # Process the payload (dummy processing here)
    result = process_spectrum(payload.dict())
    # Upload processed payload to the database
    db_result = upload_spectrum_to_db(payload.dict())
    # Merge results and return
    return {**result, **db_result}


@app.get("/api/spectra")  # , dependencies=[Depends(verify_token)])
async def get_spectra():
    """
    Returns a list of stored spectra.
    (For now, this returns an empty list.)
    """
    return {"spectra": []}


@app.get("/", response_class=HTMLResponse)
async def index():
    """
    A simple web page that displays processed spectroscopic data.
    For demonstration, it uses a dummy payload.
    """
    dummy_payload = {
        "timestamp": "2023-03-01T12:00:00Z",
        "data": [
            {"Wavenumber cm-1": 1000, "Intensities": 0.5},
            {"Wavenumber cm-1": 1100, "Intensities": 0.6},
            {"Wavenumber cm-1": 1200, "Intensities": 0.7}
        ]
    }
    processed = process_spectrum(dummy_payload)
    html_content = f"""
    <html>
      <head>
        <title>Processed Spectrum Data</title>
      </head>
      <body>
        <h1>Processed Spectrum Data</h1>
        <pre>{processed}</pre>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# You can add more endpoints as needed.
@app.get("/api/spectrum/latest/graph")  # , dependencies=[Depends(verify_token)])
async def latest_spectrum_graph():
    """
    Endpoint to display a graph of the latest spectrum.
    For demonstration, uses a dummy payload.
    """
    dummy_payload = {
        "timestamp": "2023-03-01T12:00:00Z",
        "data": [
            {"Wavenumber cm-1": 1000, "Intensities": 0.5},
            {"Wavenumber cm-1": 1100, "Intensities": 0.6},
            {"Wavenumber cm-1": 1200, "Intensities": 0.7},
            {"Wavenumber cm-1": 1300, "Intensities": 0.65},
            {"Wavenumber cm-1": 1400, "Intensities": 0.55},
        ]
    }
    return plot_latest_spectrum(dummy_payload)

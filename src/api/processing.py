# src/api/processing.py

import io
import logging
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from src.database.database import SessionLocal, Spectrum


logger = logging.getLogger("processing")
logging.basicConfig(level=logging.INFO)


def process_spectrum(payload: dict) -> dict:
    """
    Process the incoming spectroscopic payload.
    This is where calibration, ML inference, or other processing logic would be applied.

    For now, we simply log the payload and return a dummy success response.
    """
    logger.info("Processing spectrum data:")
    # logger.info(payload)

    # Simulate processing logic...
    processed_result = {
        "status": "processed",
        "message": "Spectrum data processed successfully."
    }
    return processed_result


def upload_spectrum_to_db(payload: dict) -> dict:
    """
    Uploads the given spectroscopic payload to the database.
    This function creates a new Spectrum record in the database using the payload.

    Assumes the payload includes a 'timestamp' and 'data' key.
    Returns a dict indicating success or an error message.
    """
    db = SessionLocal()
    try:
        # Create a summary from the payload data.
        summary = f"Received {len(payload.get('data', []))} data points at {payload.get('timestamp')}"
        spectrum_record = Spectrum(timestamp=payload.get("timestamp"), summary=summary)
        db.add(spectrum_record)
        db.commit()
        logger.info("Spectrum data uploaded to database successfully.")
        return {"status": "success", "message": "Spectrum data uploaded successfully."}
    except Exception as e:
        db.rollback()
        logger.error("Error uploading spectrum to database: %s", e)
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


def plot_latest_spectrum(payload: dict) -> StreamingResponse:
    """
    Generates a line graph from the spectrum data contained in the payload.
    Expects payload['data'] to be a list of dictionaries with keys "Wavenumber cm-1" and "Intensities".
    Returns a StreamingResponse with the PNG image.
    """
    data_points = payload.get("data", [])
    if not data_points:
        raise ValueError("No spectrum data available.")

    # Extract x and y values from the data points
    x = [dp.get("Wavenumber cm-1") for dp in data_points]
    y = [dp.get("Intensities") for dp in data_points]

    # Create a plot
    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o", linestyle="-")
    ax.set_title("Latest Spectrum")
    ax.set_xlabel("Wavenumber (cm-1)")
    ax.set_ylabel("Intensities")

    # Save the figure to a BytesIO buffer in PNG format
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

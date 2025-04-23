from fastapi import APIRouter
from database.database import SessionLocal, Measurement
from core.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
import pandas as pd
import json

router = APIRouter()


@router.get("/infrared/all", response_model=dict)
def get_all_infrared_measurements():
    session = SessionLocal()
    sequence = InfraredMeasurementSequence()

    try:
        # Fetch all rows
        results = session.query(Measurement).all()

        for row in results:
            spectrum_dict = row.spectrum
            # Parse JSON if it's a string (defensive coding)
            if isinstance(spectrum_dict, str):
                spectrum_dict = json.loads(spectrum_dict)

            # Build dataframe
            df = pd.DataFrame({
                'x': spectrum_dict['x'],
                'y': spectrum_dict['y']
            })

            measurement = InfraredMeasurement(df)
            measurement.time = row.timestamp
            sequence.add_measurement(measurement)

        return {
            "count": len(sequence),
            "measurements": [
                {
                    "timestamp": m.time.isoformat() if m.time else None,
                    "x_preview": m.data["x"][:5].tolist(),
                    "y_preview": m.data["y"][:5].tolist(),
                } for m in sequence
            ]
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        session.close()


@router.get("/")
def landing():
    return {
        "message": "📡 Welcome to the Spectroscopy API!",
        "endpoints": {
            "/infrared/all": "Preview all stored infrared measurements",
        }
    }

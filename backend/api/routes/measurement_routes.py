from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_gateway.database import SessionLocal, Measurement
from core.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
import pandas as pd
import json
from typing import Callable
from backend.api.services.processing.inference_service import predict_concentration


router = APIRouter()


@router.get("/predicted")
def get_predicted_concentration(model_name: str = "pls-acetone-acetonitrile"):
    """
    Endpoint to get the predicted concentration.
    """
    session = SessionLocal()
    sequence = InfraredMeasurementSequence()
    predictions = []

    try:
        results = session.query(Measurement).all()
        # load all of them into a sequence

        for row in results:
            # Parse spectrum from DB
            spectrum_dict = row.spectrum
            if isinstance(spectrum_dict, str):
                spectrum_dict = json.loads(spectrum_dict)

            df = pd.DataFrame({
                "x": spectrum_dict["x"],
                "y": spectrum_dict["y"]
            })

            measurement = InfraredMeasurement(df)
            measurement.time = row.timestamp
            sequence.add_measurement(measurement)

            try:
                concentration = predict_concentration(df["y"].tolist(), model_name)
            except Exception as e:
                concentration = None
                print(f"[Prediction error] {e}")

            predictions.append({
                "timestamp": measurement.time.isoformat() if measurement.time else None,
                "predicted_concentration": concentration
            })

        return {
            "count": len(predictions),
            "predictions": predictions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while predicting concentrations: {e}")

    finally:
        session.close()

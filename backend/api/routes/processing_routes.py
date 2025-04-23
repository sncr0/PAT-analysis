from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
import pandas as pd
import json
from typing import Callable
from backend.api.services.processing.inference_service import predict_concentration


router = APIRouter()


class ProcessingRequest(BaseModel):
    model_name: str
    payload: dict


# ---- Dispatcher route ----
@router.post("/")
def dispatch_processing(request: ProcessingRequest):
    try:
        concentration = predict_concentration(request.payload["x"], request.model_name)
        return {
            "message": "Processing dispatched successfully.",
            "predicted_concentration": concentration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during processing: {e}")

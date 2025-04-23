# src/database/database_client.py

import traceback

from db_gateway.database import SessionLocal, Measurement
from core.data_formats.spectroscopic_measurement import SpectroscopicMeasurement
from datetime import datetime


def store_measurement(measurement: SpectroscopicMeasurement, device_id: str = "Unknown"):
    """
    Commit any SpectroscopicMeasurement (infrared or raman) to the database.

    Parameters:
    - measurement: instance of InfraredMeasurement or RamanMeasurement
    - device_id: optional device identifier (str)
    """

    try:
        session = SessionLocal()

        if not isinstance(measurement, SpectroscopicMeasurement):
            raise TypeError("Only SpectroscopicMeasurement subclasses are supported.")

        if measurement.data is None:
            raise ValueError("Measurement has no spectral data.")

        spectrum_json = {
            k: v.tolist() if hasattr(v, "tolist") else v
            for k, v in measurement.data.items()
        }
        db_row = Measurement(
            device_id=device_id,
            timestamp=getattr(measurement, "time", datetime.utcnow()),
            spectrum=spectrum_json
        )

        session.add(db_row)
        session.commit()
        print(f"✅ Committed {type(measurement).__name__} at {db_row.timestamp}")
        print(f"Row ID: {db_row.id}")  # <-- verify that an ID was generated

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to commit measurement: {e}")
        traceback.print_exc()

    finally:
        session.close()

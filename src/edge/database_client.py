# src/database/database_client.py

from src.database.database import SessionLocal, Measurement
from src.data_formats.spectroscopic_measurement import SpectroscopicMeasurement
from datetime import datetime


def commit_measurement_to_db(measurement: SpectroscopicMeasurement, device_id: str = "Unknown"):
    """
    Commit any SpectroscopicMeasurement (infrared or raman) to the database.

    Parameters:
    - measurement: instance of InfraredMeasurement or RamanMeasurement
    - device_id: optional device identifier (str)
    """

    session = SessionLocal()
    try:
        if not isinstance(measurement, SpectroscopicMeasurement):
            raise TypeError("Only SpectroscopicMeasurement subclasses are supported.")

        if measurement.data is None:
            raise ValueError("Measurement has no spectral data.")

        spectrum_json = measurement.data.to_dict(orient="list")

        db_row = Measurement(
            device_id=device_id,
            timestamp=getattr(measurement, "time", datetime.utcnow()),
            spectrum=spectrum_json
        )

        session.add(db_row)
        session.commit()
        print(f"✅ Committed {type(measurement).__name__} at {db_row.timestamp}")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to commit measurement: {e}")

    finally:
        session.close()

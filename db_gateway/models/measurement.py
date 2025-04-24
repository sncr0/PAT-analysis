from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime, timezone
from db_gateway.models import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    spectrum = Column(JSON, nullable=False)

# src/database/database.py
import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from config.config import PROJECT_HOME


# ----------------------------------------------------------------------
# Environment Setup
# ----------------------------------------------------------------------


# Load env variables from global/.env
load_dotenv(dotenv_path=PROJECT_HOME)


# Read variables with fallback for robustness
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Password!1")
DB_NAME = os.getenv("POSTGRES_DB", "spectroscopy")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


# ----------------------------------------------------------------------
# SQLAlchemy Engine and Session
# ----------------------------------------------------------------------


# Full database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # Helpful for long-running MQTT or API tasks
)

Base = declarative_base()


# ----------------------------------------------------------------------
# ORM Models
# ----------------------------------------------------------------------


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    spectrum = Column(JSON, nullable=False)


# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------


def init_db(drop_existing: Optional[bool] = False) -> None:
    """
    Initialize the database schema.

    Args:
        drop_existing (bool): If True, drops and recreates all tables.
    """
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

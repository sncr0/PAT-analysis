# src/database/database.py

import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Load env variables from global/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../global/.env'))

# Read variables with fallback for robustness
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Password!1")
DB_NAME = os.getenv("POSTGRES_DB", "spectroscopy")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Full database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Sample ORM model
class Spectrum(Base):
    __tablename__ = "spectra"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    spectrum = Column(JSON, nullable=False)


# Schema init function
def init_db():
    Base.metadata.create_all(bind=engine)

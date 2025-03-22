from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use environment variables for configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/patdb")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Example model: a simple Spectrum record
class Spectrum(Base):
    __tablename__ = "spectra"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    summary = Column(String)  # A simple summary field


def init_db():
    Base.metadata.create_all(bind=engine)

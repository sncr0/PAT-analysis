from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from db_gateway.engine import engine

router = APIRouter()

@router.get("/healthz")
def healthz_check():
    return {"status": "ok"}


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/health/db", tags=["health"])
def check_database_health():
    """Health check for database connectivity."""
    connection = None
    try:
        connection = engine.connect()
        connection.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
import logging
from fastapi import APIRouter
from db_gateway.schema import init_db

logger = logging.getLogger("uvicorn")
router = APIRouter()

@router.post("/init-db")
def initialize_db(drop_existing: bool = False):
    logger.info(f"Received request to initialize DB with drop_existing={drop_existing}")
    # Simulate DB initialization
    try:
        init_db(drop_existing=drop_existing)
        logger.info("DB initialized successfully.")
        return {"status": "db initialized"}
    except Exception as e:
        logger.error(f"Failed to initialize DB: {e}")
        return {"status": "error", "message": str(e)}

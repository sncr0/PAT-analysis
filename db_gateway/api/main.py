from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from db_gateway.api.routes import health, db
from db_gateway.mqtt_listener import start_listener, stop_listener


logging.basicConfig(
    level=logging.DEBUG,  # or INFO if you prefer less noise
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main")

logger.info("🚀 Starting application setup...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: before the app starts serving
    logger.info("started mqtt")
    start_listener()
    yield
    # Shutdown: after the app is shutting down
    stop_listener()
    logger.info("stopped mqtt")


app = FastAPI(lifespan=lifespan)

# Include router
app.include_router(health.router)
app.include_router(db.router)

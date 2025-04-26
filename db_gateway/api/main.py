from fastapi import FastAPI
from db_gateway.api.routes import health, db, mqtt

app = FastAPI()

# Include router
app.include_router(health.router)
app.include_router(db.router)
app.include_router(mqtt.router)

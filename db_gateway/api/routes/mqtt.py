from fastapi import APIRouter, BackgroundTasks
from db_gateway.mqtt_listener import start as start_mqtt

router = APIRouter()

@router.post("/mqtt")
def start_mqtt_listener(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_mqtt)
    return {"status": "mqtt listener started"}
import os
import json
import logging
import signal
from datetime import datetime
import paho.mqtt.client as mqtt
from db_gateway.engine import SessionLocal
from db_gateway.models.measurement import Measurement
from db_gateway.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mqtt-listener")

# Graceful shutdown support
client = mqtt.Client()


def on_message(_client, _userdata, msg):
    logger.info(f"📥 Received message on topic '{msg.topic}'")
    session = SessionLocal()
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        spectrum = payload["spectrum"]
        timestamp = datetime.fromisoformat(payload.get("timestamp")) if "timestamp" in payload else datetime.utcnow()
        device_id = payload.get("device_id", "unknown")

        session.add(Measurement(device_id=device_id, timestamp=timestamp, spectrum=spectrum))
        session.commit()
        logger.info(f"✅ Stored measurement from '{device_id}' at {timestamp.isoformat()}")

    except Exception as e:
        logger.error(f"❌ Failed to store MQTT data: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()


def handle_shutdown(signum, frame):
    logger.warning("🛑 Shutdown signal received, disconnecting MQTT client...")
    client.disconnect()


def start(broker: str = MQTT_BROKER, port: int = MQTT_PORT, topic: str = MQTT_TOPIC):
    """
    Entry point to start the MQTT listener.
    """
    client.on_message = on_message
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        logger.info(f"📡 Connecting to MQTT broker at {broker}:{port}...")
        client.connect(broker, port)
        client.subscribe(topic)
        logger.info(f"🔄 Subscribed to '{topic}', listening for messages...")
        client.loop_forever()
    except Exception as e:
        logger.critical(f"❌ MQTT Listener crashed: {e}", exc_info=True)

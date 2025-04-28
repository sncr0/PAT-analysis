import os
import json
import logging
import socket
import time
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


def stop_listener():
    """
    Disconnects from the MQTT broker and stops the client loop.
    """
    logger.warning("🛑 Stopping MQTT listener...")
    client.loop_stop()
    client.disconnect()



def start_listener(broker: str = MQTT_BROKER, port: int = MQTT_PORT, topic: str = MQTT_TOPIC):
    """
    Connects to the MQTT broker and starts the client loop.
    Retries connection if broker is not yet available.
    """
    client.on_message = on_message
    logger.info(f"📡 Connecting to MQTT broker at {broker}:{port}...")

    retries = 5
    while retries > 0:
        try:
            client.connect(broker, port)
            break
        except (ConnectionRefusedError, socket.error) as e:
            logger.warning(f"⚠️ MQTT broker not available yet ({e}), retrying in 2s...")
            time.sleep(2)
            retries -= 1
    else:
        logger.critical("❌ Could not connect to MQTT broker after retries, giving up.")
        raise RuntimeError("MQTT broker unavailable.")

    client.subscribe(topic)
    logger.info(f"🔄 Subscribed to '{topic}', listening for messages...")
    client.loop_start()

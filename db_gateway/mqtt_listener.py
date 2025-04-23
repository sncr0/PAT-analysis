import json
import logging
import paho.mqtt.client as mqtt
from datetime import datetime
from db_gateway.database import SessionLocal, Measurement

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# Configurable constants (you can later load from .env or config.py)
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "spectroscopy/measurements"


def on_message(client, userdata, msg):
    """
    Callback function that is triggered when a message is received on the subscribed topic.
    Parses the payload and stores it in the database.
    """
    logger.info(f"📥 Received message on topic '{msg.topic}'")
    session = SessionLocal()

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        spectrum = payload["spectrum"]
        timestamp = datetime.fromisoformat(payload["timestamp"]) if payload.get("timestamp") else datetime.utcnow()
        device_id = payload.get("device_id", "Unknown")

        db_row = Measurement(
            device_id=device_id,
            timestamp=timestamp,
            spectrum=spectrum
        )
        session.add(db_row)
        session.commit()
        logger.info(f"✅ Stored MQTT measurement for device '{device_id}' at {timestamp.isoformat()}")

    except Exception as e:
        logger.error(f"❌ Failed to store MQTT data: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()


def start_listener(broker: str = MQTT_BROKER, port: int = MQTT_PORT, topic: str = MQTT_TOPIC):
    """
    Connects to the MQTT broker and listens for incoming messages on the specified topic.
    """
    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect(broker, port)
        client.subscribe(topic)
        logger.info(f"🔄 Subscribed to MQTT topic '{topic}' at {broker}:{port}")
        client.loop_forever()
    except Exception as e:
        logger.critical(f"❌ MQTT Listener failed to start: {e}", exc_info=True)


if __name__ == "__main__":
    start_listener()

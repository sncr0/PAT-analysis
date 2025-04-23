import json
import logging
import paho.mqtt.client as mqtt
from typing import Optional
from core.data_formats.spectroscopic_measurement import SpectroscopicMeasurement
from edge.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC


# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def publish_measurement(
    measurement: SpectroscopicMeasurement,
    device_id: str = "SimEdge01",
    broker_host: str = MQTT_BROKER,
    broker_port: int = MQTT_PORT,
    topic: str = MQTT_TOPIC
) -> None:
    """
    Publishes a spectroscopic measurement to the MQTT broker.

    Args:
        measurement (SpectroscopicMeasurement): Measurement data to publish.
        device_id (str): Identifier of the edge device.
        broker_host (str): MQTT broker host address.
        broker_port (int): MQTT broker port.
        topic (str): MQTT topic to publish to.
    """
    if measurement.data is None:
        raise ValueError("Measurement has no spectral data.")

    payload = {
        "device_id": device_id,
        "timestamp": measurement.time.isoformat() if measurement.time else None,
        "spectrum": {
            k: v.tolist() if hasattr(v, "tolist") else v
            for k, v in measurement.data.items()
        }
    }

    try:
        client = mqtt.Client()
        client.connect(broker_host, broker_port)
        client.loop_start()

        result = client.publish(topic, json.dumps(payload))
        result.wait_for_publish()

        logger.info(f"📤 MQTT measurement published to '{topic}' for device {device_id}")
    except Exception as e:
        logger.error(f"❌ Failed to publish measurement: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

import os

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Password!1")
DB_NAME = os.getenv("POSTGRES_DB", "spectroscopy")
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "spectroscopy/measurements")

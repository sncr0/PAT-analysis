import os

# ------------------------------------------------------------------------------
# Configuration for infrared edge‐to‐cloud pipeline
# ------------------------------------------------------------------------------

# If True, run in “simulation” mode (read CSVs).
# To override, set the environment variable SIMULATION=0 or SIMULATION=false.
SIMULATION = os.getenv("SIMULATION", "0").lower() in ("1", "true", "yes")
SIMULATION_SINE = os.getenv("SIMULATION_SINE", "1").lower() in ("1", "true", "yes")

# Folder where your simulated CSV spectra live.
# To override, set CSV_DATA_PATH=/absolute/or/relative/path
DEFAULT_CSV_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "csv")
)
CSV_DATA_PATH = os.getenv("CSV_DATA_PATH", DEFAULT_CSV_FOLDER)


# --- MQTT Broker Settings ---
MQTT_BROKER = "34.69.87.158" #os.getenv("MQTT_BROKER", "https://db-gateway-589892908719.us-central1.run.app") # "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "spectroscopy/measurements")


# ------------------------------------------------------------------------------
# End of config
# ------------------------------------------------------------------------------

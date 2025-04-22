import os

# ------------------------------------------------------------------------------
# Configuration for infrared edge‐to‐cloud pipeline
# ------------------------------------------------------------------------------

# If True, run in “simulation” mode (read CSVs).
# To override, set the environment variable SIMULATION=0 or SIMULATION=false.
SIMULATION = os.getenv("SIMULATION", "1").lower() in ("1", "true", "yes")

# Folder where your simulated CSV spectra live.
# To override, set CSV_DATA_PATH=/absolute/or/relative/path
DEFAULT_CSV_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "csv")
)
CSV_DATA_PATH = os.getenv("CSV_DATA_PATH", DEFAULT_CSV_FOLDER)

# (Optional) Cloud client settings—e.g. endpoint URL or API key.
# Uncomment & customize if needed:
# CLOUD_ENDPOINT = os.getenv("CLOUD_ENDPOINT", "https://your-cloud-endpoint")
# CLOUD_API_KEY  = os.getenv("CLOUD_API_KEY", "")

# ------------------------------------------------------------------------------
# End of config
# ------------------------------------------------------------------------------

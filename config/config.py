# config/config.py

import os
from dotenv import load_dotenv

# Load .env from same folder
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Root project path
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# You can also expose other frequently used paths
MODEL_DIR = os.path.join(PROJECT_HOME, "models")
DATA_DIR = os.path.join(PROJECT_HOME, "data")

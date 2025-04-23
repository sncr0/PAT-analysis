import numpy as np
import joblib
import os
from config.config import PROJECT_HOME, MODEL_DIR, DATA_DIR


def load_model(model_path: str):
    """Load a model given a path relative to the project root."""
    try:
        return joblib.load(model_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model at {model_path}: {e}")


def predict_concentration(x: list[float], model_name) -> float:
    """Run inference using a provided model instance."""
    model_path = os.path.join(MODEL_DIR, f"{model_name}.joblib")
    model = load_model(os.path.join(MODEL_DIR, model_path))
    X = np.array(x).reshape(1, -1)
    y_pred = model.predict(X).ravel()[0]
    return float(y_pred)

import os
import time
import numpy as np

from edge.config import SIMULATION, SIMULATION_SINE, CSV_DATA_PATH
from core.data_readers.infrared_reader import InfraredReader
from core.data_formats.infrared_measurement import InfraredMeasurement
from edge.utils import build_spectrum

# # For live spectrometer reading.
# from src.edge.spectrometer_interface import get_spectrum_data


# Import our cloud client.
from edge.cloud_client import send_datapoint
from edge.uplink import store_measurement
from edge.mqtt_uplink import publish_measurement


def run_simulation_mode():
    infraread_reader = InfraredReader()

    while True:
        try:
            acetone = infraread_reader.read_file('data/acetonitrile-acetone/67-64-1-IR.jdx')
            store_measurement(acetone)
            time.sleep(3)
        except Exception as e:
            print("Error processing simulated file:", e)


def run_simulation_mode_sine():
    print("Running in SIMULATION mode (using sine wave).")
    i = 0
    while True:
        try:
            concentration = 0.5 + 0.45 * (np.sin(i))
            print(f"Concentration: {concentration:.2f}")
            time.sleep(0.1)
            i = i + 0.1
            spectrum = build_spectrum(concentration=concentration)

            publish_measurement(spectrum)
            time.sleep(3)
        except Exception as e:
            print("Error processing simulated file:", e)


def main():
    if SIMULATION:
        run_simulation_mode()
    if SIMULATION_SINE:
        run_simulation_mode_sine()
    else:
        pass


if __name__ == "__main__":
    main()

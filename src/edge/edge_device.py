import os
import time

from src.edge.config import SIMULATION, CSV_DATA_PATH
from src.data_readers.infrared_reader import InfraredReader
from src.data_formats.infrared_measurement import InfraredDatapoint

# # For live spectrometer reading.
# from src.edge.spectrometer_interface import get_spectrum_data


# Import our cloud client.
from src.edge.cloud_client import send_datapoint
from src.edge.database_client import commit_measurement_to_db


def process_datapoint(datapoint: InfraredDatapoint):
    """
    Process a single InfraredDatapoint.
    This function prints some basic information and sends the datapoint to the cloud.
    """
    print(f"Datapoint time: {datapoint.time}")
#     print("Data preview:")
#     print(datapoint.data.head())
#     print("-" * 40)

    # Simulate sending the datapoint to the cloud.
    send_datapoint(datapoint)
    # Commit the datapoint to the database.
    commit_measurement_to_db(datapoint)


def run_simulation_mode():
    """
    Continuously reads the "last" CSV file (based on modification time)
    from CSV_DATA_PATH, processes it into an InfraredDatapoint, and sends it to the cloud.
    """
    print("Running in SIMULATION mode (using CSV files repeatedly).")
    infrared_reader = InfraredReader()

    while True:
        try:
            # List all CSV files in the simulation folder.
            files = [f for f in os.listdir(CSV_DATA_PATH) if f.endswith(".csv")]
            if not files:
                print("No CSV files found. Waiting...")
                time.sleep(2)
                continue

            # Sort files by modification time and pick the last one.
            files.sort(key=lambda f: os.path.getmtime(os.path.join(CSV_DATA_PATH, f)))
            last_file = files[-1]
            file_path = os.path.join(CSV_DATA_PATH, last_file)
            print(f"Using file: {last_file}")

            # Read the file into an InfraredDatapoint.
            datapoint = infrared_reader.read_file(file_path)
            process_datapoint(datapoint)
        except Exception as e:
            print("Error processing simulated file:", e)

        # Wait before sending the same file again.
        time.sleep(2)


def run_live_mode():
    """
    In live mode, continuously read data from the spectrometer, wrap it as an InfraredDatapoint,
    and process it.
    """
#     print("Running in LIVE mode (reading from spectrometer).")
#     while True:
#         try:
#             spectrum_df = get_spectrum_data()  # Get live data from spectrometer.
#             datapoint = InfraredDatapoint(spectrum_df)
#             # For live data, you might add a timestamp (e.g., using datetime.now())
#             datapoint.time = None  # Replace with a proper timestamp if needed.
#             process_datapoint(datapoint)
#         except Exception as e:
#             print("Error reading spectrometer data:", e)
#         # Adjust sleep to match the desired acquisition rate.
#         time.sleep(1)


def main():
    if SIMULATION:
        run_simulation_mode()
    else:
        run_live_mode()


if __name__ == "__main__":
    main()

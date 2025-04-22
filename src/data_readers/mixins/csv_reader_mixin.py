import os
from typing import Type
from datetime import timedelta
import pandas as pd
from jcamp import jcamp_readfile
from src.data_readers.mixins.format_mixin import FormatMixin
from src.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence


class CSVReaderMixin(FormatMixin):
    def _process_csv(
            self,
            file_path: str,
            measurement_class: Type[SpectroscopicMeasurement]
    ) -> tuple[pd.DataFrame, timedelta]:
        path_prefix, filename = os.path.split(file_path)
        csv_df = pd.read_csv(os.path.join(path_prefix, filename), names=['Wavenumber cm-1', 'Intensities'], skiprows=1)
        with open(os.path.join(path_prefix, filename), "r") as f:
            header = f.readline().strip()  # Read the first line and remove newline character
        measurement_time_string = header.split(',')[1]
        measurement_time = self._convert_string_to_time(measurement_time_string)
        measurement = measurement_class(csv_df)
        measurement.time = measurement_time
        return measurement

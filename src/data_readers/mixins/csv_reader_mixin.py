import os
from datetime import timedelta
import pandas as pd
from src.data_readers.mixins.format_mixin import FormatMixin


class CSVReaderMixin(FormatMixin):
    def _process_csv(self, file_path: str) -> pd.DataFrame:
        path_prefix, filename = os.path.split(file_path)
        csv_df = pd.read_csv(os.path.join(path_prefix, filename), names=['Wavenumber cm-1', 'Intensities'], skiprows=1)
        with open(os.path.join(path_prefix, filename), "r") as f:
            header = f.readline().strip()  # Read the first line and remove newline character
        datapoint_time_string = header.split(',')[1]
        datapoint_time = self._convert_string_to_time(datapoint_time_string)
        csv_df.time = datapoint_time
        return csv_df

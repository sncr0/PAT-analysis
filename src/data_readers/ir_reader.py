import os
import pandas as pd
from src.data_readers.data_reader import DataReader
from src.data_readers.mixins.csv_reader_mixin import CSVReaderMixin


class IRReader(DataReader, CSVReaderMixin):
    def __init__(self):
        self.processors = {
            "csv": self._process_csv,
        }
        self.processor = None

    def read_file(self, file_path: str) -> pd.DataFrame:
        path_prefix, filename = os.path.split(file_path)
        extension = filename.split('.')[-1]
        self.processor = self.processors.get(extension)

        ir_spectrum = self.processor(file_path)
        return ir_spectrum

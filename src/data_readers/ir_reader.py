import os
import pandas as pd
from src.data_readers.data_reader import DataReader
from src.data_readers.mixins.csv_reader_mixin import CSVReaderMixin
from src.data_formats.infrared_datapoint import InfraredDatapoint, InfraredDataSequence


class IRReader(DataReader, CSVReaderMixin):
    def __init__(self):
        super().__init__()

    def read_file(self, file_path: str) -> InfraredDatapoint:
        self._validate_file_path(file_path)
        extension = self._get_file_extension(file_path)
        self.processor = self._get_processor(extension)

        infrared_spectrum, time = self.processor(file_path)
        infrared_datapoint = InfraredDatapoint(infrared_spectrum)
        infrared_datapoint.time = time
        return infrared_datapoint

    def read_folder(self, folder_path: str) -> InfraredDataSequence:
        data_sequence = InfraredDataSequence()
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                datapoint = self.read_file(os.path.join(folder_path, file))
                data_sequence.add_datapoint(datapoint)
        return data_sequence

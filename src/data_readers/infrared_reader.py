import os
import pandas as pd
from datetime import timedelta
from typing import Callable, Type
from src.data_readers.data_reader import DataReader
from src.data_readers.mixins.csv_reader_mixin import CSVReaderMixin
from src.data_formats.infrared_datapoint import InfraredDatapoint, InfraredDataSequence


class InfraredReader(DataReader, CSVReaderMixin):
    def __init__(self):
        super().__init__()

    def read_file(
        self,
        file_path: str,
        file_processor: Callable[[str, Type[InfraredDatapoint]], InfraredDatapoint] = None
    ) -> InfraredDatapoint:
        return super().read_file(file_path, file_processor)

    def _read_file_impl(
        self,
        file_path: str,
        file_processor: Callable[[str, Type[InfraredDatapoint]], InfraredDatapoint]
    ) -> InfraredDatapoint:
        return file_processor(file_path, InfraredDatapoint)

    def _read_folder_impl(self, folder_path, file_processor):
        data_sequence = InfraredDataSequence()
        for file in os.listdir(folder_path):
            datapoint = self._read_file_impl(os.path.join(folder_path, file), file_processor)
            data_sequence.add_datapoint(datapoint)
        return data_sequence

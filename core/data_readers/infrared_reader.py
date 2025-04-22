import os
import pandas as pd
from datetime import timedelta
from typing import Callable, Type
from src.data_readers.data_reader import DataReader
from src.data_readers.mixins.csv_reader_mixin import CSVReaderMixin
from src.data_readers.mixins.jdx_reader_mixin import JCAMPDXReaderMixin
from src.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence


class InfraredReader(DataReader, CSVReaderMixin, JCAMPDXReaderMixin):
    def __init__(self):
        super().__init__()

    def read_file(
        self,
        file_path: str,
        file_processor: Callable[[str, Type[InfraredMeasurement]], InfraredMeasurement] = None
    ) -> InfraredMeasurement:
        return super().read_file(file_path, file_processor)

    def _read_file_impl(
        self,
        file_path: str,
        file_processor: Callable[[str, Type[InfraredMeasurement]], InfraredMeasurement]
    ) -> InfraredMeasurement:
        return file_processor(file_path, InfraredMeasurement)

    def _read_folder_impl(self, folder_path, file_processor) -> InfraredMeasurementSequence:
        data_sequence = InfraredMeasurementSequence()
        for file in os.listdir(folder_path):
            datapoint = self._read_file_impl(os.path.join(folder_path, file), file_processor)
            data_sequence.add_measurement(datapoint)
        return data_sequence

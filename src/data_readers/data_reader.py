from abc import ABC, abstractmethod
import os
from collections.abc import Callable
from datetime import timedelta
import pandas as pd
from src.data_readers.mixins.csv_reader_mixin import CSVReaderMixin


class DataReader(ABC, CSVReaderMixin):
    def __init__(self):
        self.processors: dict[str, Callable[[str], tuple[pd.DataFrame, timedelta]]] = {
            "csv": self._process_csv,
        }
        self.processor: Callable[[str], tuple[pd.DataFrame, timedelta]] = None

    def _get_processor(self, extension: str) -> Callable[[str], tuple[pd.DataFrame, timedelta]]:
        processor = self.processors.get(extension)
        if not processor:
            raise ValueError(f"No processor found for extension: {extension}")
        return processor

    def _get_file_extension(self, file_path: str) -> str:
        extension = file_path.split('.')[-1]
        if extension not in self.processors:
            raise ValueError(f"Unsupported file extension: {extension}")
        elif extension == "":
            raise ValueError("File has no extension.")
        return extension

    def _validate_file_path(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

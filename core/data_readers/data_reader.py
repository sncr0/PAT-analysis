from abc import ABC, abstractmethod
import os
from typing import Callable, Type
from datetime import timedelta
import pandas as pd
from core.data_readers.mixins.csv_reader_mixin import CSVReaderMixin
from core.data_readers.mixins.jdx_reader_mixin import JCAMPDXReaderMixin
from core.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence


class DataReader(CSVReaderMixin, JCAMPDXReaderMixin, ABC
                 ):
    def __init__(self):
        self.file_processors: dict[str, Callable[[str, Type[SpectroscopicMeasurement]], SpectroscopicMeasurement]] = {
            "csv": self._process_csv,
            "jdx": self._process_jdx,
        }

    def _get_file_processor(
        self,
        extension: str
    ) -> Callable[[str, Type[SpectroscopicMeasurement]], SpectroscopicMeasurement]:
        file_processor = self.file_processors.get(extension)
        if not file_processor:
            raise ValueError(f"No file processor found for extension: {extension}")
        return file_processor

    def _get_file_extension(self, file_path: str) -> str:
        if os.path.isdir(file_path):
            raise ValueError(f"Expected a file but received a directory: {file_path}")
        _, extension = os.path.splitext(file_path)
        extension = extension.lower().lstrip(".")  # Normalize
        if not extension:
            raise ValueError(f"File '{file_path}' has no extension.")
        if extension not in self.file_processors:
            raise ValueError(f"Unsupported file extension: {extension}")
        return extension

    def _validate_file_path(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if os.path.isdir(file_path):
            raise FileNotFoundError(f"Path is a folder: {file_path}")

    def _get_folder_extension(self, folder_path: str) -> str:
        self._validate_folder_path(folder_path)
        first_file = next(f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
        return self._get_file_extension(os.path.join(folder_path, first_file))

    def _validate_folder_path(self, folder_path: str) -> None:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        if not os.path.isdir(folder_path):
            raise ValueError(f"Expected a directory but received a file: {folder_path}")
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            raise ValueError(f"Folder '{folder_path}' is empty.")
        # Check that all files have the same extension
        extensions = {self._get_file_extension(os.path.join(folder_path, f)) for f in files}
        if len(extensions) > 1:
            raise ValueError(f"Inconsistent file extensions in folder '{folder_path}': {extensions}")

    def read_file(
        self,
        file_path: str,
        file_processor: Callable[[str, Type[SpectroscopicMeasurement]], SpectroscopicMeasurement] = None
    ) -> SpectroscopicMeasurement:
        if not file_processor:
            self._validate_file_path(file_path)
            extension = self._get_file_extension(file_path)
            file_processor = self._get_file_processor(extension)
        return self._read_file_impl(file_path, file_processor)

    @abstractmethod
    def _read_file_impl(self, file_path: str):  # pragma: no cover
        pass

    def read_folder(
        self,
        folder_path: str,
        file_processor: Callable[[str, Type[SpectroscopicMeasurement]], SpectroscopicMeasurement] = None
    ) -> SpectroscopicMeasurementSequence:
        if not file_processor:
            self._validate_folder_path(folder_path)
            extension = self._get_folder_extension(folder_path)
            file_processor = self._get_file_processor(extension)
        return self._read_folder_impl(folder_path, file_processor)

    @abstractmethod
    def _read_folder_impl(
        self,
        folder_path: str,
        file_processor: Callable[[str, Type[SpectroscopicMeasurement]], SpectroscopicMeasurement]
    ) -> SpectroscopicMeasurementSequence:
        pass

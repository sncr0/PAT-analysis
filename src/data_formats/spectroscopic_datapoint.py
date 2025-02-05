from abc import ABC, abstractmethod
import pandas as pd
from datetime import timedelta


class SpectroscopicDatapoint(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.time: timedelta = None


class SpectroscopicDataSequence(ABC):
    def __init__(self):
        self.data_sequence: list[SpectroscopicDatapoint] = []
        self.type = SpectroscopicDatapoint

    def _validate_type(self, datapoint: SpectroscopicDatapoint):
        if not issubclass(self.type, SpectroscopicDatapoint):
            raise RuntimeError("Data sequence object was not properly instantiated.")
        if not isinstance(datapoint, self.type):
            raise TypeError(f"Only {self.type.__name__} instances can be added.")

    def add_datapoint(self, datapoint: SpectroscopicDatapoint):
        self._validate_type(datapoint)
        return self._add_datapoint_impl(datapoint)

    @abstractmethod
    def _add_datapoint_impl(self, datapoint: SpectroscopicDatapoint):  # pragma: no cover
        """"""

    def __len__(self):
        return len(self.data_sequence)

    def __iter__(self):
        return iter(self.data_sequence)

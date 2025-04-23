from abc import ABC, abstractmethod
import pandas as pd
from datetime import timedelta


class SpectroscopicMeasurement(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.time: timedelta = None


class SpectroscopicMeasurementSequence(ABC):
    def __init__(self):
        self.measurement_sequence: list[SpectroscopicMeasurement] = []
        self.type = SpectroscopicMeasurement

    def _validate_type(self, measurement: SpectroscopicMeasurement):
        if not issubclass(self.type, SpectroscopicMeasurement):
            raise RuntimeError("Data sequence object was not properly instantiated.")
        if not isinstance(measurement, self.type):
            raise TypeError(f"Only {self.type.__name__} instances can be added.")

    def add_measurement(self, measurement: SpectroscopicMeasurement):
        self._validate_type(measurement)
        return self._add_measurement_impl(measurement)

    @abstractmethod
    def _add_measurement_impl(self, measurement: SpectroscopicMeasurement):  # pragma: no cover
        """"""

    def __len__(self):
        return len(self.measurement_sequence)

    def __iter__(self):
        return iter(self.measurement_sequence)

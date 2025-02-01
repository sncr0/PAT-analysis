from abc import ABC, abstractmethod
import pandas as pd
from datetime import timedelta


class SpectroscopicDatapoint(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.type: str = None
        self.time: timedelta = None


class SpectroscopicDataSequence(ABC):
    def __init__(self):
        self.data_sequence: list[SpectroscopicDatapoint] = []
        self.type: str = None

    def add_datapoint(self, datapoint: SpectroscopicDatapoint):
        if not isinstance(datapoint, SpectroscopicDatapoint):
            raise TypeError("Only SpectroscopicDatapoint instances can be added.")
        self.data_sequence.append(datapoint)

    def __len__(self):
        return len(self.data_sequence)

    def __iter__(self):
        return iter(self.data_sequence)

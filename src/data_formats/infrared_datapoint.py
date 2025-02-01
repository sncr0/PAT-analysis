import pandas as pd
from src.data_formats.spectroscopic_datapoint import SpectroscopicDatapoint, SpectroscopicDataSequence


class InfraredDatapoint(SpectroscopicDatapoint):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        self.type = "Infrared"


class InfraredDataSequence(SpectroscopicDataSequence):
    def __init__(self):
        super().__init__()
        self.type = "Infrared"

    def add_datapoint(self, datapoint: InfraredDatapoint):
        if not isinstance(datapoint, InfraredDatapoint):
            raise TypeError("Only InfraredDatapoint instances can be added.")
        self.data_sequence.append(datapoint)

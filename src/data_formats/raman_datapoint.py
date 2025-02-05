import pandas as pd
from src.data_formats.spectroscopic_datapoint import SpectroscopicDatapoint, SpectroscopicDataSequence


class RamanDatapoint(SpectroscopicDatapoint):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)


class RamanDataSequence(SpectroscopicDataSequence):
    def __init__(self):
        super().__init__()
        self.type = RamanDatapoint

    def _add_datapoint_impl(self, datapoint: RamanDatapoint):
        self.data_sequence.append(datapoint)

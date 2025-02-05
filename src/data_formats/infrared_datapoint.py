import pandas as pd
from src.data_formats.spectroscopic_datapoint import SpectroscopicDatapoint, SpectroscopicDataSequence


class InfraredDatapoint(SpectroscopicDatapoint):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)


class InfraredDataSequence(SpectroscopicDataSequence):
    def __init__(self):
        super().__init__()
        self.type = InfraredDatapoint

    def _add_datapoint_impl(self, datapoint: InfraredDatapoint):
        self.data_sequence.append(datapoint)

import pandas as pd
from core.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence


class RamanMeasurement(SpectroscopicMeasurement):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)


class RamanMeasurementSequence(SpectroscopicMeasurementSequence):
    def __init__(self):
        super().__init__()
        self.type = RamanMeasurement

    def _add_measurement_impl(self, measurement: RamanMeasurement):
        self.measurement_sequence.append(measurement)

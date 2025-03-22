import pandas as pd
from src.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence


class InfraredMeasurement(SpectroscopicMeasurement):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)


class InfraredMeasurementSequence(SpectroscopicMeasurementSequence):
    def __init__(self):
        super().__init__()
        self.type = InfraredMeasurement

    def _add_measurement_impl(self, measurement: InfraredMeasurement):
        self.measurement_sequence.append(measurement)

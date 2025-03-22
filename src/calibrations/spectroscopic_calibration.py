from abc import ABC, abstractmethod
from src.data_formats.spectroscopic_measurement import SpectroscopicDatapoint, SpectroscopicDataSequence


class SpectroscopicCalibration(ABC):
    def __init__(self):
        self.calibration_points: list[SpectroscopicDatapoint] = []
        self.type: SpectroscopicDatapoint = None

    def add_calibration_point(self, datapoint: SpectroscopicDatapoint):
        if not self.type:
            raise RuntimeError("Calibration object was not properly instantiated.")
        if not isinstance(datapoint, self.type):
            raise TypeError("Only SpectroscopicDatapoint instances can be added.")
        self.calibration_points.append(datapoint)

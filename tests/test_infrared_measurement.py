import pytest
import pandas as pd
from datetime import timedelta
from core.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence
from core.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
from core.data_formats.raman_measurement import RamanMeasurement, RamanMeasurementSequence


def test_spectroscopic_datapoint_initialization():
    """Test if SpectroscopicMeasurement initializes correctly."""
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredMeasurement(data)

    assert isinstance(datapoint, InfraredMeasurement)
    assert datapoint.time is None

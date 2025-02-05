import pytest
import pandas as pd
from datetime import timedelta
from src.data_formats.spectroscopic_datapoint import SpectroscopicDatapoint, SpectroscopicDataSequence
from src.data_formats.infrared_datapoint import InfraredDatapoint, InfraredDataSequence
from src.data_formats.raman_datapoint import RamanDatapoint, RamanDataSequence


def test_spectroscopic_datapoint_initialization():
    """Test if SpectroscopicDatapoint initializes correctly."""
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredDatapoint(data)

    assert isinstance(datapoint, InfraredDatapoint)
    assert datapoint.time is None

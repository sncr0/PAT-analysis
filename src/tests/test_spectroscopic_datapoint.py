import pytest
import pandas as pd
from datetime import timedelta
from src.data_formats.spectroscopic_datapoint import SpectroscopicDatapoint, SpectroscopicDataSequence
from src.data_formats.infrared_datapoint import InfraredDatapoint, InfraredDataSequence
from src.data_formats.raman_datapoint import RamanDatapoint, RamanDataSequence


def test_infrared_datapoint_initialization():
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredDatapoint(data)

    assert isinstance(datapoint, InfraredDatapoint)
    assert datapoint.time is None
    assert datapoint.data.equals(data)


def test_infrared_data_sequence_initialization():
    infrared_data_sequence = InfraredDataSequence()
    assert isinstance(infrared_data_sequence, InfraredDataSequence)
    assert infrared_data_sequence.type == InfraredDatapoint

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredDatapoint(data)
    infrared_data_sequence.add_datapoint(datapoint)
    assert len(infrared_data_sequence) == 1
    assert infrared_data_sequence.data_sequence[0] == datapoint


def test_infrared_data_sequence_iter():
    infrared_data_sequence = InfraredDataSequence()
    assert isinstance(infrared_data_sequence, InfraredDataSequence)
    assert infrared_data_sequence.type == InfraredDatapoint

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredDatapoint(data)
    infrared_data_sequence.add_datapoint(datapoint)

    for dp in infrared_data_sequence:
        assert dp == datapoint


def test_raman_datapoint_initialization():
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = RamanDatapoint(data)

    assert isinstance(datapoint, RamanDatapoint)
    assert datapoint.time is None


def test_raman_data_sequence_initialization():
    infrared_data_sequence = RamanDataSequence()
    assert isinstance(infrared_data_sequence, RamanDataSequence)
    assert infrared_data_sequence.type == RamanDatapoint

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = RamanDatapoint(data)
    infrared_data_sequence.add_datapoint(datapoint)
    assert len(infrared_data_sequence) == 1
    assert infrared_data_sequence.data_sequence[0] == datapoint


def test_raman_data_sequence_iter():
    infrared_data_sequence = RamanDataSequence()
    assert isinstance(infrared_data_sequence, RamanDataSequence)
    assert infrared_data_sequence.type == RamanDatapoint

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = RamanDatapoint(data)
    infrared_data_sequence.add_datapoint(datapoint)

    for dp in infrared_data_sequence:
        assert dp == datapoint


def test_runtime_instantiation_error():
    infrared_data_sequence = InfraredDataSequence()
    infrared_data_sequence.type = str
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = InfraredDatapoint(data)

    with pytest.raises(RuntimeError):
        infrared_data_sequence.add_datapoint(datapoint)


def test_type_error():
    infrared_data_sequence = InfraredDataSequence()
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    datapoint = RamanDatapoint(data)

    with pytest.raises(TypeError):
        infrared_data_sequence.add_datapoint(datapoint)

# def test_spectroscopic_data_sequence():
#     """Test adding datapoints to the sequence."""
#     sequence = SpectroscopicDataSequence()
#     sequence.type = InfraredDatapoint  # Set the correct type

#     data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
#     datapoint = InfraredDatapoint(data)

#     sequence.add_datapoint(datapoint)
#     assert len(sequence) == 1
#     assert sequence.data_sequence[0] == datapoint


# def test_spectroscopic_data_sequence_invalid_type():
#     """Test that adding a wrong type raises TypeError."""
#     sequence = SpectroscopicDataSequence()
#     sequence.type = InfraredDatapoint

#     data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
#     wrong_datapoint = RamanDatapoint(data)

#     with pytest.raises(TypeError):
#         sequence.add_datapoint(wrong_datapoint)

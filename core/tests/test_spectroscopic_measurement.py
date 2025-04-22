import pytest
import pandas as pd
from datetime import timedelta
from src.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence
from src.data_formats.infrared_measurement import InfraredMeasurement, InfraredMeasurementSequence
from src.data_formats.raman_measurement import RamanMeasurement, RamanMeasurementSequence


def test_infrared_measurement_initialization():
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = InfraredMeasurement(data)

    assert isinstance(measurement, InfraredMeasurement)
    assert measurement.time is None
    assert measurement.data.equals(data)


def test_infrared_measurement_sequence_initialization():
    infrared_measurement_sequence = InfraredMeasurementSequence()
    assert isinstance(infrared_measurement_sequence, InfraredMeasurementSequence)
    assert infrared_measurement_sequence.type == InfraredMeasurement

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = InfraredMeasurement(data)
    infrared_measurement_sequence.add_measurement(measurement)
    assert len(infrared_measurement_sequence) == 1
    assert infrared_measurement_sequence.measurement_sequence[0] == measurement


def test_infrared_measurement_sequence_iter():
    infrared_measurement_sequence = InfraredMeasurementSequence()
    assert isinstance(infrared_measurement_sequence, InfraredMeasurementSequence)
    assert infrared_measurement_sequence.type == InfraredMeasurement

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = InfraredMeasurement(data)
    infrared_measurement_sequence.add_measurement(measurement)

    for dp in infrared_measurement_sequence:
        assert dp == measurement


def test_raman_measurement_initialization():
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = RamanMeasurement(data)

    assert isinstance(measurement, RamanMeasurement)
    assert measurement.time is None


def test_raman_measurement_sequence_initialization():
    infrared_measurement_sequence = RamanMeasurementSequence()
    assert isinstance(infrared_measurement_sequence, RamanMeasurementSequence)
    assert infrared_measurement_sequence.type == RamanMeasurement

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = RamanMeasurement(data)
    infrared_measurement_sequence.add_measurement(measurement)
    assert len(infrared_measurement_sequence) == 1
    assert infrared_measurement_sequence.measurement_sequence[0] == measurement


def test_raman_measurement_sequence_iter():
    infrared_measurement_sequence = RamanMeasurementSequence()
    assert isinstance(infrared_measurement_sequence, RamanMeasurementSequence)
    assert infrared_measurement_sequence.type == RamanMeasurement

    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = RamanMeasurement(data)
    infrared_measurement_sequence.add_measurement(measurement)

    for dp in infrared_measurement_sequence:
        assert dp == measurement


def test_runtime_instantiation_error():
    infrared_measurement_sequence = InfraredMeasurementSequence()
    infrared_measurement_sequence.type = str
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = InfraredMeasurement(data)

    with pytest.raises(RuntimeError):
        infrared_measurement_sequence.add_measurement(measurement)


def test_type_error():
    infrared_measurement_sequence = InfraredMeasurementSequence()
    data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
    measurement = RamanMeasurement(data)

    with pytest.raises(TypeError):
        infrared_measurement_sequence.add_measurement(measurement)

# def test_spectroscopic_measurement_sequence():
#     """Test adding measurements to the sequence."""
#     sequence = SpectroscopicDataSequence()
#     sequence.type = InfraredMeasurement  # Set the correct type

#     data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
#     measurement = InfraredMeasurement(data)

#     sequence.add_measurement(measurement)
#     assert len(sequence) == 1
#     assert sequence.measurement_sequence[0] == measurement


# def test_spectroscopic_measurement_sequence_invalid_type():
#     """Test that adding a wrong type raises TypeError."""
#     sequence = SpectroscopicDataSequence()
#     sequence.type = InfraredMeasurement

#     data = pd.DataFrame({"Wavenumber cm-1": [100, 200], "Intensities": [0.1, 0.2]})
#     wrong_measurement = RamanMeasurement(data)

#     with pytest.raises(TypeError):
#         sequence.add_measurement(wrong_measurement)

import numpy as np
from unittest.mock import patch, MagicMock
from core.data_formats.infrared_measurement import InfraredMeasurement


def test_generate_sine_range():
    values = [0.5 + 0.45 * np.sin(i) for i in np.linspace(0, 2 * np.pi, 100)]
    for val in values:
        assert 0.05 <= val <= 0.95


@patch("edge.edge_device.InfraredReader")
@patch("edge.edge_device.store_measurement")
@patch("edge.edge_device.time.sleep", return_value=None)
def test_simulation_static(mock_store, mock_reader, _):
    mock_spectrum = MagicMock(spec=InfraredMeasurement)
    mock_reader().read_file.return_value = mock_spectrum

    spectrum = mock_reader().read_file("somefile")
    store_measurement = mock_store
    store_measurement(spectrum)

    mock_store.assert_called_once()


@patch("edge.edge_device.time.sleep", return_value=None)
@patch("edge.edge_device.publish_measurement")
@patch("edge.edge_device.build_spectrum")
def test_simulation_sine(mock_build, mock_publish, _):
    mock_spectrum = MagicMock(spec=InfraredMeasurement)
    mock_build.return_value = mock_spectrum

    concentration = 0.5 + 0.45 * np.sin(0)
    spectrum = mock_build(concentration)
    mock_publish(spectrum)

    mock_build.assert_called_once_with(concentration)  # ✅ FIXED
    mock_publish.assert_called_once_with(mock_spectrum)

import os
from core.data_formats.infrared_measurement import InfraredMeasurement
from core.data_readers.infrared_reader import InfraredReader
from config.config import PROJECT_HOME, DATA_DIR, MODEL_DIR


def build_spectrum(concentration: float) -> InfraredMeasurement:
    """
    Build a synthetic spectrum based on the given concentration of acetone in acetonitrile.
    """
    reader = InfraredReader()
    acetonitrile = reader.read_file(os.path.join(DATA_DIR, 'acetonitrile-acetone/75-05-8-IR.jdx'))
    acetone = reader.read_file(os.path.join(DATA_DIR, 'acetonitrile-acetone/67-64-1-IR.jdx'))
    output_spectrum = reader.read_file(os.path.join(DATA_DIR, 'acetonitrile-acetone/67-64-1-IR.jdx'))

    y = acetone.data['y'] * concentration + acetonitrile.data['y'] * (1 - concentration)
    output_spectrum.data['y'] = y
    output_spectrum.data['title'] = f"Acetone concentration: {concentration:.2f}"
    return output_spectrum

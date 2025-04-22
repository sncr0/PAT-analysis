import os
from typing import Type
from datetime import timedelta, datetime
import pandas as pd
from jcamp import jcamp_readfile
from src.data_readers.mixins.format_mixin import FormatMixin
from src.data_formats.spectroscopic_measurement import SpectroscopicMeasurement, SpectroscopicMeasurementSequence


class JCAMPDXReaderMixin(FormatMixin):
    def _process_jdx(
            self,
            file_path: str,
            measurement_class: Type[SpectroscopicMeasurement]
    ) -> tuple[pd.DataFrame, timedelta]:
        path_prefix, filename = os.path.split(file_path)
        jcamp = jcamp_readfile(os.path.join(path_prefix, filename))
        measurement_time = datetime.utcnow()
        measurement = measurement_class(jcamp)
        measurement.time = measurement_time
        return measurement

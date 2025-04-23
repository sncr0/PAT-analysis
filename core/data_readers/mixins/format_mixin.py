from abc import ABC, abstractmethod
from datetime import timedelta


class FormatMixin(ABC):
    def _convert_string_to_time(self, time_string: str) -> timedelta:
        h, m, s = map(int, time_string.split(":"))
        time_object = timedelta(hours=h, minutes=m, seconds=s)
        return time_object

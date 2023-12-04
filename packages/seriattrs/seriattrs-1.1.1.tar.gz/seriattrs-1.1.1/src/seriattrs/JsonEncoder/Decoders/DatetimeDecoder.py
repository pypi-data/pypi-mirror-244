from datetime import datetime

from ...JsonEncoder import Decoder


class DatetimeDecoder(Decoder):
    @staticmethod
    def is_valid(field_type: type) -> bool:
        return field_type == datetime

    @staticmethod
    def decode(element: str, _) -> datetime:
        if isinstance(element, datetime):
            return element
        return datetime.fromtimestamp(float(element))



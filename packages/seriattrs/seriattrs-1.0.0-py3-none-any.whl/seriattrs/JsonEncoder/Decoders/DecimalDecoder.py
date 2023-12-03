from decimal import Decimal
from typing import Any

from ...JsonEncoder import Decoder
from ...db_attrs_converter import db_attrs_converter


class DecimalDecoder(Decoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return element == Decimal

    @staticmethod
    def decode(element: Any, _) -> Decimal:
        return Decimal(element)


db_attrs_converter.register_structure_hook(Decimal, DecimalDecoder.decode)

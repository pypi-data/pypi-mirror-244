from enum import Enum
from typing import Any

from ...JsonEncoder.Encoder import Encoder


class EnumEncoder(Encoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return isinstance(element, Enum)

    @staticmethod
    def encode(element: Enum) -> str:
        from ..DefaultJsonEncoder import DefaultJsonEncoder

        return eval(DefaultJsonEncoder().encode(element.value))

from enum import Enum
from typing import Any, TypeVar, Type

from ...JsonEncoder import Decoder

T = TypeVar('T', bound=Enum)


class EnumDecoder(Decoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return issubclass(element, Enum)

    @staticmethod
    def decode(element: Any, enum: Type[T]) -> T:
        return enum(element)

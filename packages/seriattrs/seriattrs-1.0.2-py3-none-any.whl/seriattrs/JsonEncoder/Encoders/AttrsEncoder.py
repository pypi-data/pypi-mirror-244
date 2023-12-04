import json
from typing import Any

from attr import has, asdict

from ...JsonEncoder import Encoder


class AttrsEncoder(Encoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return has(element)

    @staticmethod
    def encode(element) -> dict:
        from ..DefaultJsonEncoder import DefaultJsonEncoder

        return json.loads(json.dumps(asdict(element), cls=DefaultJsonEncoder))

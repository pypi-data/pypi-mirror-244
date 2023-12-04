from functools import partial

from attr import field, validators


def _check_int(instance, attribute, value, bits: int):
    if value < -(2 ** (bits - 1)):
        raise ValueError(f"{value=} must be more than {-(2 ** (bits - 1))}")
    if value > 2 ** (bits - 1) - 1:
        raise ValueError(f"{value=} must be less than {2 ** (bits - 1) - 1}")


def _check_uint(instance, attribute, value, bits: int):
    if value < 0:
        raise ValueError(f"{value=} must be positive")
    if value > 2**bits - 1:
        raise ValueError(f"{value=} must be less than {2 ** bits - 1}")


int8 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=8)]
)
int16 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=16)]
)
int32 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=32)]
)
int64 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=64)]
)
uint8 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=8)]
)
uint16 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=16)]
)
uint32 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=32)]
)
uint64 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=64)]
)

from functools import partial

from attr import field, validators, NOTHING


def _check_char(instance, attribute, value, length: int):
    if len(value) != length:
        raise ValueError(f"Length of {value=} must be {length} is {len(value)}")


def _check_varchar(instance, attribute, value, max_length: int):
    if len(value) > max_length:
        raise ValueError(
            f"Length of {value=} must be less than {max_length} is {len(value)}"
        )


def char(
    length: int,
    *,
    default=NOTHING,
    validator=None,
    repr=True,
    hash=None,
    init=True,
    metadata=None,
    type=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    alias=None,
):
    return partial(
        field,
        validator=[validators.instance_of(str), partial(_check_char, length=length)]
        if validator is None
        else validator,
    )(
        default=default,
        repr=repr,
        hash=hash,
        init=init,
        metadata=metadata,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
        alias=alias,
        type=type,
    )


def varchar(
    max_length: int,
    *,
    default=NOTHING,
    validator=None,
    repr=True,
    hash=None,
    init=True,
    metadata=None,
    type=None,
    converter=None,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=None,
    alias=None,
):
    return partial(
        field,
        validator=[
            validators.instance_of(str),
            partial(_check_varchar, max_length=max_length),
        ]
        if validator is None
        else validator,
    )(
        default=default,
        repr=repr,
        hash=hash,
        init=init,
        metadata=metadata,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
        alias=alias,
        type=type,
    )


text = partial(field, validator=[validators.instance_of(str)])

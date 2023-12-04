import re
import typing
from collections import defaultdict
from inspect import signature
from typing import Any, get_args, ForwardRef

from attr import fields


class DbClassCreator(type):
    def __new__(cls, name: str, bases: tuple, namespace: dict[str, Any]):
        new_class = super().__new__(cls, name, bases, namespace)
        for field_name, field_type in new_class.__annotations__.items():
            forward_refs = _get_forward_refs(field_type)
            for forward_ref in forward_refs:
                if forward_ref in created_types:
                    new_class.__annotations__[field_name] = _update_hint(forward_ref, str(new_class.__annotations__[field_name]))
                else:
                    type_checked_fields[forward_ref].append(new_class)
        created_types[ForwardRef(name)] = new_class
        for db_class in type_checked_fields.get(ForwardRef(name), []):
            attrs_fields = []
            for f in fields(db_class):
                forward_refs = _get_forward_refs(f.type)
                current_string_type = f.type
                for forward_ref in forward_refs:
                    if forward_ref not in created_types:
                        continue
                    current_string_type = _update_hint(forward_ref, current_string_type)
                field_value = dict((arg, getattr(f, arg)) for arg in signature(type(f)).parameters if hasattr(f, arg))
                field_value['type'] = current_string_type
                field_value['cmp'] = None
                new_field = type(f)(**field_value)
                attrs_fields.append(new_field)
            db_class.__attrs_attrs__ = type(db_class.__attrs_attrs__)(attrs_fields)
        return new_class


def _get_forward_refs(field_type):
    forward_refs = list(ref for ref in get_args(field_type) if isinstance(ref, ForwardRef))
    if isinstance(field_type, str):
        forward_refs.append(ForwardRef(field_type))
    return forward_refs


def _update_hint(forward_ref: ForwardRef, current_string_type: str):
    forward_ref_name = created_types[forward_ref].__name__
    return eval(
        re.sub(fr'ForwardRef\(\'{forward_ref_name}\'\)', forward_ref_name, current_string_type),
        globals(), {forward_ref_name: created_types[forward_ref]}
    )


type_checked_fields: defaultdict[ForwardRef, list[DbClassCreator]] = defaultdict(list)
created_types: dict[ForwardRef, DbClassCreator] = {}
__all__ = [
    'typing'
]

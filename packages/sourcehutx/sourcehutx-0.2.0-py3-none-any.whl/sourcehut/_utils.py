# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from collections.abc import Callable, Iterator, MutableMapping, Sequence
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ValidationError, validator

from .exceptions import ResourceNotFoundError

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    _T = TypeVar("_T")
    _P = ParamSpec("_P")

_MappingT = TypeVar("_MappingT", bound=MutableMapping)


def filter_ellipsis(mapping: _MappingT) -> _MappingT:
    for key, value in tuple(mapping.items()):
        if value is ...:
            mapping.pop(key)
    return mapping


def get_locals(**mapping: Any) -> dict[str, Any]:
    renames: dict[str, str] = mapping.pop("renames", {})
    return {
        renames.get(key, key): int(value) if key.endswith("id") else value
        for key, value in mapping.items()
        if key != "self" and not key.startswith("_")
    }


def infinite_iter() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1


def _v_submitter(cls, value: Any) -> Any:  # noqa: ARG001
    if isinstance(value, str):
        return value
    try:
        value = value["canonicalName"]
    except KeyError:
        return value
    try:
        return value.lstrip("~")
    except AttributeError:
        return value


def v_submitter(*args, **kwargs):
    return validator(*args, **kwargs, pre=True, allow_reuse=True)(_v_submitter)


def v_comma_separated_list(*args: Any, **kwargs: Any):
    def inner(cls, value: Any):  # noqa: ARG001
        if not isinstance(value, str):
            return value
        return value.split(",")

    return validator(*args, **kwargs, pre=True, allow_reuse=True)(inner)


def _v_client(cls, value: Any, values: dict[str, Any]):  # noqa: ARG001
    client = values["client"]
    if not value.client:
        value.client = client
    return value


def v_client(*args, **kwargs):
    return validator(*args, **kwargs, allow_reuse=True)(_v_client)


def check_found(data: _T) -> _T:
    if data is None:
        raise ResourceNotFoundError
    return data


def get_key(mapping, *keys: Sequence):
    for key in keys:
        if mapping is None:
            raise ResourceNotFoundError
        mapping = mapping[key]
    if mapping is None:
        raise ResourceNotFoundError
    return mapping


def try_types(*types: type[_T]) -> Callable[..., _T]:
    def inner(**__obj: Any) -> _T:
        for typ in types:
            try:
                return typ(**__obj)
            except ValidationError:
                continue
        raise TypeError(f"Failed to coerce object into {types}")

    return inner

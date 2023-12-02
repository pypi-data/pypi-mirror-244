# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
SrhtClient exception classes
"""

from __future__ import annotations

from contextlib import suppress
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    _T = TypeVar("_T")
    import httpx


def _get_err_msgs(data: dict[str, Any] | None) -> list[str]:
    if not data:
        return []
    errors: list[str] = []
    for error in data.get("errors", ()):
        if isinstance(error, dict) and "message" in error:
            errors.append(error["message"])
    return errors


class SrhtError(Exception):
    """
    Exception base class for SrhtClient errors
    """


class ResourceNotFoundError(SrhtError):
    """
    The requested resource was not available
    """


class SrhtClientError(SrhtError):
    """
    Exception for HTTP errors in the Sourcehut client
    """

    def __init__(self, request: httpx.Request, response: httpx.Response) -> None:
        self.request = request
        self.response = response
        self.json: dict[str, Any] | None = None
        with suppress(JSONDecodeError):
            self.json = self.response.json()
        self.errors: list[str] = _get_err_msgs(self.json)

    def __str__(self) -> str:
        msg = (
            f"Recieved {self.response.status_code} {self.response.reason_phrase}"
            f" from {self.request.url}"
        )
        if self.errors:
            msg += ": " + ", ".join(self.errors or [])
        return msg

    def __repr__(self) -> str:
        cls = type(self).__name__
        request = self.request
        response = self.response
        json = self.json
        errors = self.errors
        return f"{cls}({request=}, {response=}, {json=}, {errors=})"

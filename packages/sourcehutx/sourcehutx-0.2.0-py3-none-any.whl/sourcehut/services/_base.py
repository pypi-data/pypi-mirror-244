# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Base classes for Sourcehut services
"""

from __future__ import annotations

from abc import ABCMeta
from collections.abc import AsyncIterator, Callable, Sequence
from typing import Any, Generic, TypeVar, Union

from pydantic import BaseModel, Field

from .._utils import check_found as _cf
from .._utils import get_key as _get_key
from .._utils import infinite_iter
from ..client import SRHT_SERVICE, APIVersion, SrhtClient

_ServiceClientT = TypeVar("_ServiceClientT", bound="_ServiceClient")
_BaseResourceT = TypeVar("_BaseResourceT", bound="_BaseResource")
_ResourceT = TypeVar("_ResourceT", bound="_Resource")
_UserRefT = TypeVar("_UserRefT", bound="_UserRef")

_USER_REF_MEMBERS = """\
id
canonicalName
username
email
"""


class _ServiceClient(metaclass=ABCMeta):
    SERVICE: SRHT_SERVICE

    def __init__(self, client: SrhtClient) -> None:
        self.client = client
        self._whoami: str | None = None

    async def whoami(self) -> str:
        if not self._whoami:
            self._whoami = await self.client.whoami(self.SERVICE)
        return self._whoami

    async def _u(self, username: str | None) -> str:
        if username:
            return username
        return await self.whoami()

    async def version(self) -> APIVersion:
        return await self.client.version(self.SERVICE)

    async def query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        *,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self.client.query(
            self.SERVICE, query, variables, extra_params=extra_params
        )

    async def _cursorit(
        self,
        key: str | Sequence[str],
        typ: type[_BaseResourceT] | Callable[..., _BaseResourceT],
        query: str,
        max_pages: int | None,
        variables: dict[str, Any] | None = None,
        extra_kwargs: dict | None = None,
    ) -> AsyncIterator[_BaseResourceT]:
        if isinstance(key, str):
            key = [key]
        variables = variables or {}
        extra_kwargs = extra_kwargs or {}
        cursor: str | None = None

        for _ in range(max_pages) if max_pages else infinite_iter():
            json = await self.query(query, {**variables, "cursor": cursor})
            json = _get_key(json, *key)
            cursor = json["cursor"]
            for resource in json["results"]:
                yield typ(**resource, **extra_kwargs, client=self)
            if not cursor:
                break


class _BaseResource(BaseModel, Generic[_ServiceClientT], arbitrary_types_allowed=True):
    client: Union[_ServiceClientT, None] = Field(None, exclude=True)

    @property
    def _client(self) -> _ServiceClientT:
        if not self.client:
            raise ValueError("self.client is unset!")
        return self.client


class _Resource(_BaseResource[_ServiceClientT], Generic[_ServiceClientT]):
    id: int

    def __int__(self) -> int:
        return self.id


async def _get_user_ref(
    client: _ServiceClient,
    typ: type[_UserRefT],
    username: Union[str, _UserRef, None],
) -> _UserRefT:
    username = await client._u(str(username) if username is not None else None)
    query = (
        """
    query getUserRef($username: String!) {
        user(username: $username) {
            %s
        }
    }
    """
        % _USER_REF_MEMBERS
    )
    json = await client.query(query, {"username": username})
    return typ(**_cf(json["user"]), client=client)  # type: ignore[call-arg]


class _UserRef(BaseModel):
    id: int
    username: str
    email: str
    canonical_name: str = Field(alias="canonicalName")

    def __str__(self) -> str:
        return self.username

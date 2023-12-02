# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT


from __future__ import annotations

import dataclasses
import os
from collections.abc import Sequence
from enum import Enum
from json import dumps as json_dumps
from typing import IO, TYPE_CHECKING, Any, NamedTuple, TypeVar

import httpx

from .config import DEFAULT_BASEURL
from .exceptions import ResourceNotFoundError, SrhtClientError

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from .config import SrhtConfig

    _FileContentType: TypeAlias = "str|bytes|IO[bytes]"

_NOT_FOUND = "the requested element is null which the schema does not allow"


class SRHT_SERVICE(str, Enum):
    GIT = "git"
    HG = "hg"
    BUILDS = "builds"
    TODO = "todo"
    LISTS = "lists"
    MAN = "man"
    META = "meta"
    PASTE = "paste"
    PAGES = "pages"
    # Not yet implemented by upstream
    # HUB = "hub"

    def __str__(self) -> str:
        return self.value


class VISIBILITY(str, Enum):
    PUBLIC = "PUBLIC"
    UNLISTED = "UNLISTED"
    PRIVATE = "PRIVATE"

    def __str__(self) -> str:
        return self.value


class APIVersion(NamedTuple):
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclasses.dataclass(frozen=True)
class _FileUpload:
    content: _FileContentType
    filename: str | os.PathLike[str] | None

    def _get_tuple(self) -> tuple[str, _FileContentType] | _FileContentType:
        return (str(self.filename), self.content) if self.filename else self.content


def _get_upload_data(
    query: str,
    variables: dict[str, Any],
    uploads: dict[str, _FileUpload | Sequence[_FileUpload]],
) -> tuple[
    # data
    dict[str, dict[str, Any]],
    # files
    dict[str, _FileContentType | tuple[str, _FileContentType]],
]:
    variables = variables.copy()
    file_index: int = 0
    files: dict[str, _FileContentType | tuple[str, _FileContentType]] = {}
    data_map: dict[str, list[str]] = {}

    for variable, file in uploads.items():
        if isinstance(file, _FileUpload):
            files[str(file_index)] = file._get_tuple()
            data_map[str(file_index)] = [f"variables.{variable}"]
            variables[variable] = variables.get(variable, None)
            file_index += 1
        else:
            variables[variable] = variables.get(variable, [None] * len(file))
            for index, current_file in enumerate(file):
                files[str(file_index)] = current_file._get_tuple()
                data_map[str(file_index)] = [f"variables.{variable}.{index}"]
                file_index += 1

    data_operations: dict[str, Any] = {"query": query, "variables": variables}

    data: dict[str, dict[str, Any]] = {
        "operations": data_operations,
        "map": data_map,
    }
    return data, files


_ClientT = TypeVar("_ClientT", bound="SrhtClient")


class SrhtClient:
    """
    Async client for the Sourcehut GraphQL API
    """

    def __init__(
        self,
        baseurl: str,
        token: str,
        http_client: httpx.AsyncClient | None = None,
        *,
        protocol: str = "https://",
    ) -> None:
        self.http_client = http_client or httpx.AsyncClient()
        self.baseurl = baseurl
        self.token = token
        self.protocol = protocol

    async def __aenter__(self: _ClientT) -> _ClientT:
        return self

    async def __aexit__(self, *_) -> None:
        await self.http_client.aclose()

    @classmethod
    def from_config(
        cls: type[_ClientT], config: SrhtConfig, client: httpx.AsyncClient | None = None
    ) -> _ClientT:
        if not config.api_token:
            raise ValueError("api_token is not provided in the config")
        return cls(config.baseurl, config.api_token, client, protocol=config.protocol)

    def get_endpoint(self, service: SRHT_SERVICE) -> str:
        return f"{self.protocol}{service}.{self.baseurl}/query"

    @property
    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    async def query(
        self,
        service: SRHT_SERVICE,
        query: str,
        variables: dict[str, Any] | None = None,
        *,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        # data = {"operations": json_dumps(payload)}
        extra_params = extra_params or {}

        endpoint = self.get_endpoint(service)
        headers = dict(**extra_params.pop("headers", {}), **self.auth_headers)

        resp = await self.http_client.post(
            endpoint,
            json=payload,
            headers=headers,
            follow_redirects=True,
            **extra_params,
        )
        return self._handle_error(resp)

    async def _query_with_upload(
        self,
        service: SRHT_SERVICE,
        query: str,
        variables: dict[str, Any],
        uploads: dict[str, _FileUpload | Sequence[_FileUpload]],
        *,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        extra_params = extra_params or {}
        endpoint = self.get_endpoint(service)
        headers = dict(**extra_params.pop("headers", {}), **self.auth_headers)

        data, files = _get_upload_data(query, variables, uploads)
        encoded_data: dict[str, str] = {
            key: json_dumps(value) for key, value in data.items()
        }

        resp = await self.http_client.post(
            endpoint,
            data=encoded_data,
            files=files,
            headers=headers,
            follow_redirects=True,
            **extra_params,
        )
        json = self._handle_error(resp)
        return json

    def _handle_error(self, resp: httpx.Response) -> dict[str, Any]:
        if resp.is_error:
            raise SrhtClientError(resp.request, resp)
        json: dict[str, Any] = resp.json()
        if json.get("errors"):
            exc = SrhtClientError(resp.request, resp)
            if exc.errors == [_NOT_FOUND]:
                raise ResourceNotFoundError
            else:
                raise exc
        return json["data"]

    async def whoami(self, service: SRHT_SERVICE) -> str:
        query = """
        query {
          me {
            username
          }
        }
        """
        data = await self.query(service, query)
        return data["me"]["username"]

    async def version(self, service: SRHT_SERVICE) -> APIVersion:
        query = """
        query {
          version {
            major
            minor
            patch
          }
        }
        """
        data = await self.query(service, query)
        return APIVersion(**data["version"])

    def __repr__(self) -> str:
        cls = type(self).__name__
        http_client, baseurl, protocol = self.http_client, self.baseurl, self.protocol
        return f"{cls}({baseurl=}, token='XXXXXXX', {http_client=}, {protocol=})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SrhtClient):
            return False
        # fmt: off
        return (
            (self.baseurl, self.token, self.protocol) ==
            (other.baseurl, other.token, other.protocol)
        )
        # fmt: on


__all__ = (
    "SRHT_SERVICE",
    "VISIBILITY",
    "APIVersion",
    "SrhtClient",
    "DEFAULT_BASEURL",
)

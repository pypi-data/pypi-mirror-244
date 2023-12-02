# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
pages.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime as DT
from enum import Enum
from typing import IO, Any, Dict, List, Optional, Union

from pydantic import Field, validator

from .._utils import check_found as _cf
from .._utils import get_locals
from ..client import SRHT_SERVICE, _FileUpload
from ._base import _Resource, _ServiceClient

_SITE_REF_MEMBERS = """\
id
domain
protocol
"""

_SITE_MEMBERS = (
    _SITE_REF_MEMBERS
    + """\
created
updated
version
notFound
"""
)


class SITE_PROTOCOL(str, Enum):
    HTTPS = "https"
    GEMINI = "gemini"

    def __str__(self) -> str:
        return self.value


@dataclass()
class FileConfig:
    glob: str
    cache_control: Optional[str] = None

    def get_dict(self) -> Dict[str, Any]:
        return {"glob": self.glob, "options": {"cacheControl": self.cache_control}}


@dataclass()
class _SiteConfig:
    not_found: Optional[str] = None
    file_configs: Optional[List[FileConfig]] = None

    def get_dict(self) -> Dict[str, Any]:
        return {
            "notFound": self.not_found,
            "fileConfigs": [config.get_dict() for config in self.file_configs]
            if self.file_configs is not None
            else None,
        }


class PagesSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.PAGES

    async def publish(
        self,
        domain: str,
        content: Union[bytes, IO[bytes]],
        protocol: SITE_PROTOCOL = SITE_PROTOCOL.HTTPS,
        subdirectory: Optional[str] = None,
        not_found: Optional[str] = None,
        file_configs: Optional[List[FileConfig]] = None,
    ) -> Site:
        inp = get_locals(**locals())
        inp["siteConfig"] = _SiteConfig(
            inp.pop("not_found"), inp.pop("file_configs")
        ).get_dict()
        inp["protocol"] = str(inp["protocol"]).upper()
        del inp["content"]
        query = (
            """
        mutation publish(
            $domain: String!
            $file: Upload!
            $protocol: Protocol!
            $subdirectory: String
            $siteConfig: SiteConfig
        ) {
            publish(
                domain: $domain
                content: $file
                protocol: $protocol
                subdirectory: $subdirectory
                siteConfig: $siteConfig
            ) {
                %s
            }
        }

        """
            % _SITE_MEMBERS
        )
        upload = _FileUpload(content, None)
        data = await self.client._query_with_upload(
            self.SERVICE, query, inp, {"file": upload}
        )
        return Site(**_cf(data["publish"]), client=self)

    async def unpublish(
        self, domain: str, protocol: SITE_PROTOCOL = SITE_PROTOCOL.HTTPS
    ) -> Site:
        inp = get_locals(**locals())
        inp["protocol"] = str(inp["protocol"]).upper()
        query = (
            """
        mutation unpublish(
            $domain: String!
            $protocol: Protocol!
        ) {
            unpublish(
                domain: $domain
                protocol: $protocol
            ) {
                %s
            }
        }
        """
            % _SITE_MEMBERS
        )
        data = await self.query(query, inp)
        return Site(**_cf(data["unpublish"]), client=self)

    def list_sites(self, *, max_pages: Optional[int] = 1) -> AsyncIterator[Site]:
        query = (
            """
        query listSites(
            $cursor: Cursor
        ) {
            sites(cursor: $cursor) {
                cursor
                results {
                    %s
                }
            }
        }
        """
            % _SITE_MEMBERS
        )
        return self._cursorit("sites", Site, query, max_pages)


class SiteRef(_Resource[PagesSrhtClient]):
    domain: str
    protocol: SITE_PROTOCOL

    @validator("protocol", pre=True)
    def _v_site_ref(cls, value: Any) -> Any:
        if value == "":  # noqa: PLC1901 # Other falsy values should cause an error
            value = SITE_PROTOCOL.HTTPS
        return value


class Site(SiteRef):
    created: DT
    updated: DT
    version: str
    not_found: Optional[str] = Field(None, alias="notFound")

    async def unpublish(self) -> Site:
        return await self._client.unpublish(self.domain, self.protocol)


__all__ = ("SITE_PROTOCOL", "FileConfig", "SiteRef", "Site")

# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
paste.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from datetime import datetime as DT
from typing import List, Optional

from .._utils import check_found as _cf
from .._utils import v_submitter
from ..client import SRHT_SERVICE, VISIBILITY
from ..client import _FileUpload as FileUpload
from ._base import _BaseResource, _ServiceClient

_PASTE_REF_MEMBERS = """
id
user {
    canonicalName
}
"""
_PASTE_MEMBERS = (
    _PASTE_REF_MEMBERS
    + """
created
visibility
files {
    filename
    hash
    contents
}
"""
)


class PasteSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.PASTE

    async def create(
        self, files: Sequence[FileUpload], visibility: VISIBILITY = VISIBILITY.UNLISTED
    ) -> Paste:
        query = (
            """
        mutation createPaste($files: [Upload!]!, $visibility: Visibility!) {
            create(files: $files, visibility: $visibility) {
                %s
            }
        }
        """
            % _PASTE_MEMBERS
        )
        variables = {"visibility": visibility}
        json = await self.client._query_with_upload(
            self.SERVICE, query, variables, {"files": files}
        )
        return Paste(**_cf(json["create"]), client=self)

    async def delete(self, paste_id: str | PasteRef) -> Paste:
        variables = {"paste_id": str(paste_id)}
        query = (
            """
        mutation delete($paste_id: String!) {
            delete(id: $paste_id) {
                %s
            }
        }
        """
            % _PASTE_MEMBERS
        )

        json = await self.query(query, variables)
        return Paste(**_cf(json["delete"]), client=self)

    async def get_paste_ref(self, paste_id: str | PasteRef) -> PasteRef:
        query = (
            """
        query getPasteRef($paste_id: String!) {
            paste(id: $paste_id) {
                %s
            }
        }
        """
            % _PASTE_REF_MEMBERS
        )
        variables = {"paste_id": str(paste_id)}
        json = await self.query(query, variables)
        return PasteRef(**_cf(json["paste"]), client=self)

    async def get_paste(self, paste_id: str | PasteRef) -> Paste:
        query = (
            """
        query getPaste($paste_id: String!) {
            paste(id: $paste_id) {
                %s
            }
        }
        """
            % _PASTE_MEMBERS
        )
        variables = {"paste_id": str(paste_id)}
        json = await self.query(query, variables)
        return Paste(**_cf(json["paste"]), client=self)

    async def list_pastes(
        self, username: Optional[str] = None, *, max_pages: Optional[int] = 1
    ) -> AsyncIterator[Paste]:
        username = await self._u(username)
        query = (
            """
        query listPastes($username: String!, $cursor: Cursor) {
            user(username: $username) {
                pastes(cursor: $cursor) {
                    cursor
                    results {
                        %s
                    }
                }
            }
        }
        """
            % _PASTE_MEMBERS
        )
        async for paste in self._cursorit(
            ["user", "pastes"], Paste, query, max_pages, {"username": username}
        ):
            yield paste


class File(_BaseResource[PasteSrhtClient]):
    filename: Optional[str]
    hash: str
    contents: str


class PasteRef(_BaseResource[PasteSrhtClient]):
    id: str
    user: str
    _v_user = v_submitter("user")

    async def delete(self) -> Paste:
        return await self._client.delete(self.id)

    async def get(self) -> Paste:
        return await self._client.get_paste(self)

    def __str__(self) -> str:
        return self.id


class Paste(PasteRef):
    created: DT
    visibility: VISIBILITY
    files: List[File]


__all__ = ("FileUpload", "PasteSrhtClient", "File", "PasteRef", "Paste")

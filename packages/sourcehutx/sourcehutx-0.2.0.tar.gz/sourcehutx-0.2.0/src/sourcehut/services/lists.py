# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

from __future__ import annotations

from datetime import datetime as DT
from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import Field

from .._utils import check_found as _cf
from .._utils import filter_ellipsis
from .._utils import get_key as _g
from .._utils import get_locals, v_comma_separated_list, v_submitter
from ..client import SRHT_SERVICE, VISIBILITY
from ._base import _get_user_ref, _Resource, _ServiceClient, _UserRef

_LIST_REF_MEMBERS = """
id
name
owner {
    canonicalName
}

"""
_LIST_MEMBERS = (
    _LIST_REF_MEMBERS
    + """
created
updated
description
visibility
permitMime
rejectMime
archive
last30days
"""
)

if TYPE_CHECKING:
    pass
else:
    ellipsis = type(...)


class ListsSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.LISTS

    async def create_list(
        self,
        name: str,
        description: Optional[str] = None,
        visibility: VISIBILITY = VISIBILITY.PUBLIC,
    ) -> MailingList:
        inp = get_locals(**locals())
        query = (
            """
        mutation createList(
            $name: String!
            $description: String
            $visibility: Visibility!
        ) {
            createMailingList(
                name: $name
                description: $description
                visibility: $visibility
            ) {
                %s
            }
        }
        """
            % _LIST_MEMBERS
        )
        data = await self.query(query, inp)
        return MailingList(**data["createMailingList"], client=self)

    async def delete_list(self, listid: Union[int, MailingListRef]) -> MailingList:
        query = (
            """
        mutation deleteList(
            $listid: Int!
        ) {
            deleteMailingList(
                id: $listid
            ) {
                %s
            }
        }
        """
            % _LIST_MEMBERS
        )
        data = await self.query(query, {"listid": int(listid)})
        return MailingList(**_cf(data["deleteMailingList"]), client=self)

    async def get_list_ref(self, username: Optional[str], name: str) -> MailingListRef:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = (
            """
        query getListRef($username: String!, $name: String!) {
            user(username: $username) {
                list(name: $name) {
                    %s
                }
            }
        }
        """
            % _LIST_REF_MEMBERS
        )
        data = await self.query(query, inp)
        return MailingListRef(**_g(data, "user", "list"), client=self)

    async def get_list(self, username: Optional[str], name: str) -> MailingList:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = (
            """
        query getList($username: String!, $name: String!) {
            user(username: $username) {
                list(name: $name) {
                    %s
                }
            }
        }
        """
            % _LIST_MEMBERS
        )
        data = await self.query(query, inp)
        return MailingList(**_g(data, "user", "list"), client=self)

    async def update_list(
        self,
        listid: Union[int, MailingListRef],
        description: Union[str, None, ellipsis] = ...,
        visibility: Union[VISIBILITY, ellipsis] = ...,
    ) -> MailingList:
        inp = filter_ellipsis(get_locals(**locals()))
        listid = inp.pop("listid")
        query = (
            """
        mutation updateList(
            $listid: Int!
            $inp: MailingListInput!
        ) {
            updateMailingList(
                id: $listid
                input: $inp
            ) {
                %s
            }
        }
        """
            % _LIST_MEMBERS
        )
        data = await self.query(query, {"listid": listid, "inp": inp})
        return MailingList(**_cf(data["updateMailingList"]), client=self)

    async def get_user_ref(self, username: Union[str, _UserRef, None]) -> UserRef:
        return await _get_user_ref(self, UserRef, username)


class MailingListRef(_Resource[ListsSrhtClient]):
    owner: str
    name: str
    _v_owner = v_submitter("owner")

    async def delete(self) -> MailingList:
        return await self._client.delete_list(self)

    async def update(
        self,
        description: Union[str, None, ellipsis] = ...,
        visibility: Union[VISIBILITY, ellipsis] = ...,
    ) -> MailingList:
        return await self._client.update_list(self, description, visibility)

    async def get(self) -> MailingList:
        return await self._client.get_list(self.owner, self.name)


class MailingList(MailingListRef):
    created: DT
    updated: DT
    description: Optional[str]
    visibility: VISIBILITY
    permit_mime: List[str] = Field(alias="permitMime")
    reject_mime: List[str] = Field(alias="rejectMime")
    archive: str
    last_30_days: str = Field(alias="last30days")
    _v_permit_mime = v_comma_separated_list("permit_mime")
    _v_reject_mime = v_comma_separated_list("reject_mime")


class UserRef(_UserRef, _Resource[ListsSrhtClient]):
    ...


__all__ = ("ListsSrhtClient", "MailingListRef", "MailingList", "UserRef")

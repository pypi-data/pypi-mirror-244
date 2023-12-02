# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
meta.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime as DT
from typing import Optional, Union

from pydantic import Field

from .._utils import check_found as _cf
from .._utils import get_locals, v_submitter
from ..client import SRHT_SERVICE
from ._base import _Resource, _ServiceClient, _UserRef

_PGPKey_REF_MEMBERS = """
id
user {
    canonicalName
}
fingerprint
"""
_PGPKey_MEMBERS = (
    _PGPKey_REF_MEMBERS
    + """
created
lastUsed
key
comment
"""
)


_SSHKey_REF_MEMBERS = """\
id
user {
    canonicalName
}
fingerprint
"""
_SSHKey_MEMBERS = (
    _SSHKey_REF_MEMBERS
    + """\
created
lastUsed
key
comment
"""
)

_USER_REF_MEMBERS = """\
id
canonicalName
username
email
"""
_USER_MEMBERS = (
    _USER_REF_MEMBERS
    + """\
created
updated
url
location
bio
"""
)

_AUDIT_LOG_ENTRY_MEMBERS = """\
id
created
ipAddress
eventType
details
"""

_INVOICE_MEMBERS = """\
id
created
cents
validThru
source
"""


class MetaSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.META

    async def create_pgp_key(self, key: str) -> PGPKey:
        inp = get_locals(**locals())
        query = (
            """
        mutation create($key: String!) {
            createPGPKey(key: $key) {
                %s
            }
        }
        """
            % _PGPKey_MEMBERS
        )
        json = await self.query(query, inp)
        return PGPKey(**json["createPGPKey"], client=self)

    async def get_pgp_key(self, fingerprint: Union[str, PGPKeyRef]) -> PGPKey:
        query = (
            """
        query getKey($fingerprint: String!) {
            pgpKeyByFingerprint(fingerprint: $fingerprint) {
                %s
            }
        }
        """
            % _PGPKey_MEMBERS
        )
        json = await self.query(query, {"fingerprint": str(fingerprint)})
        return PGPKey(**_cf(json["pgpKeyByFingerprint"]), client=self)

    async def get_pgp_key_ref(self, fingerprint: Union[str, PGPKeyRef]) -> PGPKeyRef:
        query = (
            """
        query getKeyRef($fingerprint: String!) {
            pgpKeyByFingerprint(fingerprint: $fingerprint) {
                %s
            }
        }
        """
            % _PGPKey_REF_MEMBERS
        )
        json = await self.query(query, {"fingerprint": str(fingerprint)})
        return PGPKeyRef(**_cf(json["pgpKeyByFingerprint"]), client=self)

    async def delete_pgp_key(self, key_id: Union[int, PGPKeyRef]) -> PGPKey:
        inp = get_locals(**locals())
        query = (
            """
        mutation deletePGPKey($key_id: Int!) {
            deletePGPKey(id: $key_id) {
                %s
            }
        }
        """
            % _PGPKey_MEMBERS
        )
        json = await self.query(query, inp)
        return PGPKey(**_cf(json["deletePGPKey"]), client=self)

    def list_pgp_keys(
        self, *, max_pages: Optional[int] = None
    ) -> AsyncIterator[PGPKey]:
        query = (
            """
        query listPGPKeys($cursor: Cursor) {
            me {
                pgpKeys(cursor: $cursor) {
                    cursor
                    results {
                        %s
                    }
                }
            }
        }
        """
            % _PGPKey_MEMBERS
        )
        return self._cursorit(["me", "pgpKeys"], PGPKey, query, max_pages)

    async def create_ssh_key(self, key: str) -> SSHKey:
        inp = get_locals(**locals())
        query = (
            """
        mutation createSSHKey($key: String!) {
            createSSHKey(key: $key) {
                %s
            }
        }
        """
            % _SSHKey_MEMBERS
        )
        json = await self.query(query, inp)
        return SSHKey(**json["createSSHKey"], client=self)

    async def get_ssh_key(self, fingerprint: Union[str, SSHKeyRef]) -> SSHKey:
        inp = {"fingerprint": str(fingerprint)}
        query = (
            """
        query getSSHKey($fingerprint: String!) {
            sshKeyByFingerprint(fingerprint: $fingerprint) {
                %s
            }
        }
        """
            % _SSHKey_MEMBERS
        )
        json = await self.query(query, inp)
        return SSHKey(**_cf(json["sshKeyByFingerprint"]), client=self)

    async def get_ssh_key_ref(self, fingerprint: Union[str, SSHKeyRef]) -> SSHKeyRef:
        inp = {"fingerprint": str(fingerprint)}
        query = (
            """
        query getSSHKey($fingerprint: String!) {
            sshKeyByFingerprint(fingerprint: $fingerprint) {
                %s
            }
        }
        """
            % _SSHKey_REF_MEMBERS
        )
        json = await self.query(query, inp)
        return SSHKeyRef(**_cf(json["sshKeyByFingerprint"]), client=self)

    def list_ssh_keys(self, *, max_pages: Optional[int] = 1) -> AsyncIterator[SSHKey]:
        query = (
            """
        query listSSHKeys($cursor: Cursor) {
            me {
                sshKeys(cursor: $cursor) {
                    cursor
                    results {
                        %s
                    }
                }
            }
        }
        """
            % _SSHKey_MEMBERS
        )
        return self._cursorit(["me", "sshKeys"], SSHKey, query, max_pages)

    async def delete_ssh_key(self, key_id: Union[int, SSHKeyRef]) -> SSHKey:
        inp = get_locals(**locals())
        query = (
            """
        mutation deleteSSHKey($key_id: Int!) {
            deleteSSHKey(id: $key_id) {
                %s
            }
        }
        """
            % _SSHKey_MEMBERS
        )
        json = await self.query(query, inp)
        return SSHKey(**_cf(json["deleteSSHKey"]), client=self)

    async def get_user(self, username: Union[str, UserRef, None] = None) -> User:
        username = await self._u(str(username) if username is not None else None)
        query = (
            """
        query getUser($username: String!) {
            userByName(username: $username) {
                %s
            }
        }
        """
            % _USER_MEMBERS
        )
        json = await self.query(query, {"username": username})
        return User(**_cf(json["userByName"]), client=self)

    async def get_user_ref(self, username: Union[str, UserRef, None] = None) -> UserRef:
        username = await self._u(str(username) if username is not None else None)
        query = (
            """
        query getUserRef($username: String!) {
            userByName(username: $username) {
                %s
            }
        }
        """
            % _USER_REF_MEMBERS
        )
        json = await self.query(query, {"username": username})
        return UserRef(**_cf(json["userByName"]), client=self)

    def audit_log(
        self, *, max_pages: Optional[int] = 1
    ) -> AsyncIterator[AuditLogEntry]:
        query = (
            """
        query auditLog($cursor: Cursor) {
            auditLog(cursor: $cursor) {
                ursor
                results {
                    %s
                }
            }
        }
        """
            % _AUDIT_LOG_ENTRY_MEMBERS
        )
        return self._cursorit(["auditLog"], AuditLogEntry, query, max_pages)

    def list_invoices(self, *, max_pages: Optional[int] = 1) -> AsyncIterator[Invoice]:
        query = (
            """
        query listInvoices($cursor: Cursor) {
            invoices(cursor: $cursor) {
                cursor
                results {
                    %s
                }
            }
        }
        """
            % _INVOICE_MEMBERS
        )
        return self._cursorit(["invoices"], Invoice, query, max_pages)


class PGPKeyRef(_Resource[MetaSrhtClient]):
    user: str
    fingerprint: str
    _v_user = v_submitter("user")

    def __str__(self) -> str:
        return self.fingerprint

    async def get(self) -> PGPKey:
        return await self._client.get_pgp_key(self)

    async def delete(self) -> PGPKey:
        return await self._client.delete_pgp_key(self)


class PGPKey(PGPKeyRef):
    created: DT
    last_used: Optional[DT] = Field(alias="lastUsed")
    key: str
    comment: Optional[str]


class SSHKeyRef(_Resource[MetaSrhtClient]):
    user: str
    fingerprint: str
    _v_user = v_submitter("user")

    def __str__(self) -> str:
        return self.fingerprint

    async def get(self) -> SSHKey:
        return await self._client.get_ssh_key(self)

    async def delete(self) -> SSHKey:
        return await self._client.delete_ssh_key(self)


class SSHKey(SSHKeyRef):
    created: DT
    last_used: Optional[DT] = Field(alias="lastUsed")
    key: str
    comment: Optional[str]


class UserRef(_UserRef, _Resource[MetaSrhtClient]):
    async def get(self) -> User:
        return await self._client.get_user(self)


class User(UserRef):
    created: DT
    updated: DT
    url: Optional[str]
    location: Optional[str]
    bio: Optional[str]


class AuditLogEntry(_Resource[MetaSrhtClient]):
    created: DT
    ip_address: str = Field(alias="ipAddress")
    event_type: str = Field(alias="eventType")
    details: Optional[str]


class Invoice(_Resource[MetaSrhtClient]):
    created: DT
    cents: int
    valid_thru: DT = Field(alias="validThru")
    source: Optional[str]

    @property
    def price(self) -> float:
        return self.cents / 100


__all__ = (
    "MetaSrhtClient",
    "PGPKeyRef",
    "PGPKey",
    "SSHKeyRef",
    "SSHKey",
    "UserRef",
    "AuditLogEntry",
    "User",
    "Invoice",
)

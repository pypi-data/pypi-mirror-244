# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
import respx

from sourcehut.client import SrhtClient
from sourcehut.services import meta

INVOICE_DATA_1: dict[str, Any] = {
    "id": 1234567,
    "created": "2023-08-13T16:33:23.55834Z",
    "cents": 2000,
    "validThru": "2024-08-13T00:00:00Z",
    "source": "Nice try!",
}
INVOICE_JSON = {"data": {"invoices": {"cursor": None, "results": [INVOICE_DATA_1]}}}

AUDIT_LOG_DATA_1: dict[str, Any] = {
    "id": 123445678,
    "created": "2023-08-13T16:33:23.55834Z",
    "ipAddress": "1.1.1.1",
    "eventType": "xyz",
    "details": None,
}
AUDIT_LOG_JSON = {"data": {"auditLog": {"cursor": None, "results": [AUDIT_LOG_DATA_1]}}}

USER_REF_DATA_1: dict[str, Any] = {
    "id": 1234,
    "canonicalName": "~person",
    "username": "person",
    "email": "person@person.xyz",
}
USER_REF_JSON = {"data": {"userByName": USER_REF_DATA_1}}
USER_DATA_1: dict[str, Any] = {
    **USER_REF_DATA_1,
    "created": "2023-08-13T16:33:23.55834Z",
    "updated": "2023-08-13T16:33:23.55834Z",
    "url": None,
    "location": "Somewhere, Someplace",
    "bio": "A person.",
}
USER_REF_JSON = {"data": {"userByName": USER_DATA_1}}

# Borrowed for both SSH and PGP keys
SSH_KEY_FINGERPRINT = "ad:81:a1:49:d1:08:84:99:30:dc:ac:a7:e3:ec:f0:3f"
SSH_KEY_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK2h3LqD9UYubrKs0962ekYub3qxi6wPHbWrMCg0xPCB python-sourcehut tests"  # noqa: E501
SSH_KEY_REF_DATA_1: dict[str, Any] = {
    "id": 123456,
    "fingerprint": SSH_KEY_FINGERPRINT,
    "user": {"canonicalName": "~person"},
}
SSH_KEY_DATA_1: dict[str, Any] = {
    **SSH_KEY_REF_DATA_1,
    "created": "2023-08-13T16:33:23.55834Z",
    "lastUsed": None,
    "key": SSH_KEY_KEY,
    "comment": "python-sourcehut tests",
}


@pytest.mark.asyncio
async def test_meta_list_invoices(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(json=INVOICE_JSON)
            gotten = [invoice async for invoice in client.list_invoices()]
            expected = meta.Invoice(**INVOICE_DATA_1, client=client)
            assert expected.price == 20.00
            assert gotten == [expected]
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_auditlog(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(json=AUDIT_LOG_JSON)
            gotten = [entry async for entry in client.audit_log()]
            expected = meta.AuditLogEntry(**AUDIT_LOG_DATA_1, client=client)
            assert gotten == [expected]
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_user_ref(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            with patch.object(client, "_u", return_value="person") as mocked:
                endpoint = client.client.get_endpoint(client.SERVICE)
                route = respx_mock.post(endpoint).respond(json=USER_REF_JSON)
                expected = meta.UserRef(**USER_REF_DATA_1, client=client)

                gotten = await client.get_user_ref()
                assert gotten == expected
                assert route.call_count == 1
                mocked.assert_called_once_with(None)

                gotten = await client.get_user_ref(gotten)
                assert route.call_count == 2
                mocked.assert_called_with("person")


@pytest.mark.asyncio
async def test_meta_create_ssh_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"createSSHKey": SSH_KEY_DATA_1}}
            )
            key = await client.create_ssh_key(SSH_KEY_KEY)
            expected = meta.SSHKey(**SSH_KEY_DATA_1, client=client)
            assert key == expected
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_list_ssh_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={
                    "data": {
                        "me": {"sshKeys": {"cursor": None, "results": [SSH_KEY_DATA_1]}}
                    }
                }
            )
            keys = [k async for k in client.list_ssh_keys()]
            expected = meta.SSHKey(**SSH_KEY_DATA_1, client=client)
            assert expected in keys
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_get_ssh_key_ref(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"sshKeyByFingerprint": SSH_KEY_REF_DATA_1}}
            )
            ref = await client.get_ssh_key_ref(SSH_KEY_FINGERPRINT)
            expected = meta.SSHKeyRef(**SSH_KEY_REF_DATA_1, client=client)
            assert ref == expected

            ref2 = await client.get_ssh_key_ref(ref)
            assert ref2 == ref

            assert route.call_count == 2


@pytest.mark.asyncio
async def test_meta_get_ssh_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"sshKeyByFingerprint": SSH_KEY_DATA_1}}
            )
            key = await client.get_ssh_key(SSH_KEY_FINGERPRINT)
            expected = meta.SSHKey(**SSH_KEY_DATA_1, client=client)
            assert key == expected

            key2 = await key.get()
            assert key2 == key

            assert route.call_count == 2


@pytest.mark.asyncio
async def test_meta_create_gpg_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"createPGPKey": SSH_KEY_DATA_1}}
            )
            key = await client.create_pgp_key(SSH_KEY_KEY)
            expected = meta.PGPKey(**SSH_KEY_DATA_1, client=client)
            assert key == expected
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_list_pgp_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={
                    "data": {
                        "me": {"pgpKeys": {"cursor": None, "results": [SSH_KEY_DATA_1]}}
                    }
                }
            )
            keys = [k async for k in client.list_pgp_keys()]
            expected = meta.PGPKey(**SSH_KEY_DATA_1, client=client)
            assert expected in keys
            assert route.call_count == 1


@pytest.mark.asyncio
async def test_meta_get_pgp_key_ref(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"pgpKeyByFingerprint": SSH_KEY_REF_DATA_1}}
            )
            ref = await client.get_pgp_key_ref(SSH_KEY_FINGERPRINT)
            expected = meta.PGPKeyRef(**SSH_KEY_REF_DATA_1, client=client)
            assert ref == expected

            ref2 = await client.get_pgp_key_ref(ref)
            assert ref2 == ref

            assert route.call_count == 2


@pytest.mark.asyncio
async def test_meta_get_pgp_key(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = meta.MetaSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"pgpKeyByFingerprint": SSH_KEY_DATA_1}}
            )
            key = await client.get_pgp_key(SSH_KEY_FINGERPRINT)
            expected = meta.PGPKey(**SSH_KEY_DATA_1, client=client)
            assert key == expected

            key2 = await key.get()
            assert key2 == key

            assert route.call_count == 2

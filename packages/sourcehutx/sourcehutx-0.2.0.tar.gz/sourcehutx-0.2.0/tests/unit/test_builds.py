# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import datetime
from typing import Any

import pytest
import pytest_asyncio
import respx

from sourcehut.client import SrhtClient
from sourcehut.services import builds

FAKE_DATE_1 = "2023-08-11T06:00:02.050859Z"
FAKE_DATE_1_DT = datetime.datetime(
    2023, 8, 11, 6, 0, 2, 50859, tzinfo=datetime.timezone.utc
)
FAKE_DATE_2 = "2023-08-11T06:03:50.753334Z"
FAKE_DATE_2_DT = datetime.datetime(
    2023, 8, 11, 6, 3, 50, 753334, tzinfo=datetime.timezone.utc
)

JOB_DATA_1: dict[str, Any] = {
    "id": 1039160,
    "created": FAKE_DATE_1,
    "updated": FAKE_DATE_2,
    "status": "SUCCESS",
    "manifest": "",
    "note": "",
    "tags": ["fedora-scripts", "scheduled", "go-leaves"],
    "visibility": "PUBLIC",
    "image": "fedora/rawhide",
    "runner": None,
    "owner": {"canonicalName": "~person"},
}
SECRET_DATA = {"id": 12345, "created": FAKE_DATE_1, "uuid": "12345", "name": "test key"}
SECRET_FILE_DATA = {
    **SECRET_DATA,
    "name": "test file",
    "path": "abcd/123",
    "mode": 0o600,
}


def SECRET_DATA_OBJ(**kwargs):
    return builds.Secret(
        id=12345, created=FAKE_DATE_1_DT, uuid="12345", name="test key", **kwargs
    )


def SECRET_FILE_OBJ(**kwargs):
    return builds.SecretFile(
        id=12345,
        created=FAKE_DATE_1_DT,
        uuid="12345",
        name="test file",
        path="abcd/123",
        mode=0o600,
        **kwargs,
    )


@pytest_asyncio.fixture
async def client(fake_srht_client: SrhtClient) -> builds.BuildsSrhtClient:
    return builds.BuildsSrhtClient(fake_srht_client)


@pytest.mark.asyncio
async def test_builds_get_build(client: builds.BuildsSrhtClient):
    with respx.mock() as respx_mock:
        endpoint = client.client.get_endpoint(client.SERVICE)
        route = respx_mock.post(endpoint).respond(json={"data": {"job": JOB_DATA_1}})
        gotten = await client.get_job(1039160)
        assert gotten == builds.Job(**JOB_DATA_1, client=client)
        assert route.call_count == 1
        second = await gotten.get()
        assert second == gotten
        assert route.call_count == 2
        status = await client.get_job_status(gotten)
        assert status.succeeded
        assert route.call_count == 3


@pytest.mark.asyncio
async def test_builds_list_secrets(client: builds.BuildsSrhtClient):
    with respx.mock() as respx_mock:
        endpoint = client.client.get_endpoint(client.SERVICE)
        route = respx_mock.post(endpoint).respond(
            json={
                "data": {
                    "secrets": {
                        "cursor": None,
                        "results": [
                            SECRET_DATA,
                            SECRET_FILE_DATA,
                            SECRET_FILE_DATA,
                            SECRET_DATA,
                        ],
                    }
                }
            }
        )
        results = [secret async for secret in client.list_secrets()]
        expected = [
            SECRET_DATA_OBJ(client=client),
            SECRET_FILE_OBJ(client=client),
            SECRET_FILE_OBJ(client=client),
            SECRET_DATA_OBJ(client=client),
        ]
        assert results == expected
        assert route.call_count == 1


def test_builds_job_status():
    pending = builds.JOB_STATUS.PENDING
    assert pending.in_progress
    assert not pending.succeeded
    assert not pending.failed
    assert str(pending) == "PENDING"

    assert builds.JOB_STATUS.SUCCESS.succeeded
    assert builds.JOB_STATUS.TIMEOUT.failed

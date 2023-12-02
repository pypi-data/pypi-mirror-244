# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import pytest
import respx

from sourcehut.client import (
    SRHT_SERVICE,
    APIVersion,
    SrhtClient,
    _FileUpload,
    _get_upload_data,
)

if TYPE_CHECKING:
    from sourcehut.client import _FileContentType

TEST_FILE_1 = b"TEST_FILE_1\n"
TEST_FILE_2 = "TEST_FILE_2\n"


def test_client_dunder():
    client = SrhtClient("sourcehut.example", "abcd", protocol="http://")
    assert client != "jfjfjffjf"
    assert client == SrhtClient("sourcehut.example", "abcd", protocol="http://")

    rep = repr(client.http_client)
    assert repr(client) == (
        "SrhtClient("
        "baseurl='sourcehut.example', token='XXXXXXX',"
        f" http_client={rep}, protocol='http://')"
    )


@pytest.mark.asyncio
async def test_client_version(fake_srht_client: SrhtClient):
    data = {"data": {"version": {"major": 1, "minor": 1, "patch": 0}}}
    endpoint = fake_srht_client.get_endpoint(SRHT_SERVICE.GIT)
    with respx.mock() as respx_mock:
        route = respx_mock.post(endpoint).respond(json=data)
        version = await fake_srht_client.version(SRHT_SERVICE.GIT)
        # Check that mock was used
        assert route.call_count == 1
        # Check expected versions
        assert version == APIVersion(1, 1, 0)
        # Check __str__
        assert str(version) == "1.1.0"


@pytest.mark.parametrize(
    "uploads, variables, operations_map, files",
    [
        pytest.param(
            {"file": _FileUpload(TEST_FILE_1, "test_file_1.txt")},
            {"file": None},
            {"0": ["variables.file"]},
            {"0": ("test_file_1.txt", TEST_FILE_1)},
            id="basic-single-file",
        ),
        pytest.param(
            {"uploads": [_FileUpload(content=TEST_FILE_1, filename="test_file_1.txt")]},
            {"uploads": [None]},
            {"0": ["variables.uploads.0"]},
            {"0": ("test_file_1.txt", TEST_FILE_1)},
            id="list-single-file",
        ),
        pytest.param(
            {
                "uploads": [
                    _FileUpload(content=TEST_FILE_1, filename="test_file_1.txt"),
                    _FileUpload(content=TEST_FILE_2, filename="test_file_2.txt"),
                ]
            },
            {"uploads": [None, None]},
            {"0": ["variables.uploads.0"], "1": ["variables.uploads.1"]},
            {
                "0": ("test_file_1.txt", TEST_FILE_1),
                "1": ("test_file_2.txt", TEST_FILE_2),
            },
            id="list-multiple-file",
        ),
    ],
)
def test_client_get_upload_data(
    uploads: dict[str, _FileUpload | Sequence[_FileUpload]],
    variables: dict[str, Any],
    operations_map: dict[str, list[str]],
    files: dict[str, _FileContentType | tuple[str, _FileContentType]],
):
    gotten_data, gotten_files = _get_upload_data("", {}, uploads)
    assert gotten_data["operations"] == {"variables": variables, "query": ""}
    assert gotten_data["map"] == operations_map
    assert gotten_files == files

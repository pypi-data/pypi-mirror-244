# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
paste.sr.ht API
"""

from __future__ import annotations

import hashlib
import sys

import pytest
import pytest_asyncio

from sourcehut.client import VISIBILITY, SrhtClient
from sourcehut.services import paste

from .. import vcr


def sha1(item: bytes) -> str:
    hash_obj: hashlib._Hash
    if sys.version_info >= (3, 9):
        hash_obj = hashlib.sha1(item, usedforsecurity=False)
    else:
        hash_obj = hashlib.sha1(item)
    return hash_obj.hexdigest()


TEST_FILE_1 = b"TEST_FILE_1\n"
TEST_FILE_1_HASH = sha1(TEST_FILE_1)
TEST_FILE_2 = b"TEST_FILE_2\n"
TEST_FILE_2_HASH = sha1(TEST_FILE_2)


@pytest_asyncio.fixture()
async def client(srht_client: SrhtClient) -> paste.PasteSrhtClient:
    return paste.PasteSrhtClient(srht_client)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_create_paste(authed_client: SrhtClient):
    client = paste.PasteSrhtClient(authed_client)
    gotten = await client.create(
        [
            paste.FileUpload(TEST_FILE_1, "test_file_1.py"),
            paste.FileUpload(TEST_FILE_2, "test_file_2.py"),
        ]
    )
    try:
        user = await client.whoami()
        expected = paste.Paste(
            client=client,
            id=gotten.id,
            user=user,
            created=gotten.created,
            visibility=VISIBILITY.UNLISTED,
            files=[
                paste.File(
                    filename="test_file_1.py",
                    contents=gotten.files[0].contents,
                    hash=TEST_FILE_1_HASH,
                    client=None,
                ),
                paste.File(
                    filename="test_file_2.py",
                    contents=gotten.files[1].contents,
                    hash=TEST_FILE_2_HASH,
                    client=None,
                ),
            ],
        )
        assert expected == gotten

        # Check get_paste and get_paste_ref
        ref = await client.get_paste_ref(expected)
        gotten2 = await ref.get()
        assert gotten2.dict(exclude={"created"}) == gotten.dict(exclude={"created"})

        # Check list_pastes
        all_pastes = [p.dict(exclude={"created"}) async for p in client.list_pastes()]
        assert gotten.dict(exclude={"created"}) in all_pastes
    finally:
        await gotten.delete()

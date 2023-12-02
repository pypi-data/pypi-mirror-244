# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any

import pytest
import pytest_asyncio

from sourcehut.client import VISIBILITY, SrhtClient
from sourcehut.services import lists

from .. import vcr


@pytest_asyncio.fixture()
async def client(srht_client: SrhtClient) -> lists.ListsSrhtClient:
    return lists.ListsSrhtClient(srht_client)


@pytest.mark.asyncio
@vcr.use_cassette()
async def test_create_list(client: lists.ListsSrhtClient):
    mailing_list = await client.create_list("testlist", "This is a test list")
    try:
        whoami = await client.whoami()
        permitMime = "text/*,application/pgp-signature,application/pgp-keys"
        expected = lists.MailingList(
            id=mailing_list.id,
            name="testlist",
            owner=whoami,
            created=mailing_list.created,
            updated=mailing_list.updated,
            description="This is a test list",
            visibility=VISIBILITY.PUBLIC,
            permitMime=permitMime,  # type: ignore[arg-type]
            rejectMime="text/html",  # type: ignore[arg-type]
            archive=mailing_list.archive,
            last30days=mailing_list.last_30_days,
            client=client,
        )
        assert mailing_list == expected

        ref = await client.get_list_ref(whoami, "testlist")
        gotten = await ref.get()
        assert gotten == mailing_list

        # Ensure updating list with nothing leaves the same result
        cases: list[tuple[Any, ...]] = [
            # (),
            ("This is a test list",),
            ("This is a test list", VISIBILITY.PUBLIC),
            (..., VISIBILITY.PUBLIC),
        ]
        for data in cases:
            gotten = await mailing_list.update(*data)
            mailing_list.updated = gotten.updated
            assert gotten == mailing_list
    finally:
        await mailing_list.delete()

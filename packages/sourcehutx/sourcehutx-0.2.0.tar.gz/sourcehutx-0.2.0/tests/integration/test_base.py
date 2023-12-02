# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import dataclasses

import pytest

from sourcehut.client import SrhtClient
from sourcehut.services import _base, git, lists, meta, todo

from .. import vcr


@dataclasses.dataclass()
class Service:
    client_type: type[_base._ServiceClient]
    user_ref_type: type[_base._UserRef]


SERVICES: tuple[Service, ...] = (
    Service(git.GitSrhtClient, git.UserRef),
    Service(lists.ListsSrhtClient, lists.UserRef),
    Service(meta.MetaSrhtClient, meta.UserRef),
    Service(todo.TodoSrhtClient, todo.UserRef),
)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_base_get_user(srht_client: SrhtClient):
    for service in SERVICES:
        client = service.client_type(srht_client)

        user_ref = await client.get_user_ref(  # type: ignore[attr-defined]
            "gotmax23-test"
        )
        expected_ref = service.user_ref_type(  # type: ignore[call-arg]
            client=client,
            username="gotmax23-test",
            email="maxwell+client-test@gtmx.me",
            canonicalName="~gotmax23-test",
            id=user_ref.id,
        )
        assert user_ref.dict(include={"client"}) == expected_ref.dict(
            include={"client"}
        )

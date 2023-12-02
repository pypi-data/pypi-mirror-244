# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import pytest
import pytest_asyncio

from sourcehut.client import SrhtClient
from sourcehut.config import SrhtConfig

from . import ROOT

CONFIG = ROOT / "python-sourcehut.toml"


@pytest.fixture()
def authed_client() -> SrhtClient:
    if CONFIG.exists():
        config = SrhtConfig.read_config(CONFIG)
    else:
        config = SrhtConfig(api_token="XXXXXXX")
    client = SrhtClient.from_config(config)
    return client


@pytest_asyncio.fixture()
async def srht_client(authed_client):
    async with authed_client:
        yield authed_client


@pytest.fixture()
def fake_client() -> SrhtClient:
    config = SrhtConfig(api_token="XXXXXXX")
    client = SrhtClient.from_config(config)
    return client


@pytest_asyncio.fixture()
async def fake_srht_client(fake_client):
    async with fake_client:
        yield fake_client

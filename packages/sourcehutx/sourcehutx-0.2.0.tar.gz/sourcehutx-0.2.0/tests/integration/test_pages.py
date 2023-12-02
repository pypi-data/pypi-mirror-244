# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
pages.sr.ht API
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio

from sourcehut.client import SrhtClient
from sourcehut.services import pages

from .. import ROOT, vcr


@pytest_asyncio.fixture()
async def client(srht_client: SrhtClient) -> pages.PagesSrhtClient:
    return pages.PagesSrhtClient(srht_client)


@pytest.mark.asyncio
@pytest.mark.xfail(
    reason="The cassettes contain binary data"
    " and require a patched vcrpy to handle them"
)
@vcr.use_cassette
async def test_pages_publish(authed_client: SrhtClient, tmp_path: Path):
    async with authed_client:
        client = pages.PagesSrhtClient(authed_client)
        content = (ROOT / "fixtures/test_site.tar.gz").read_bytes()
        whoami = await client.whoami()
        domain = f"{whoami}.srht.site"
        site = await client.publish(
            f"{whoami}.srht.site",
            content,
            subdirectory="python-sourcehut-test",
        )
        try:
            expected = pages.Site(
                id=site.id,
                client=client,
                domain=domain,
                protocol=pages.SITE_PROTOCOL.HTTPS,
                created=site.created,
                updated=site.updated,
                version=site.version,
                notFound=None,
            )
            assert site == expected

            gotten = [s async for s in client.list_sites()]
            assert site in gotten
        finally:
            await site.unpublish()


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param(
            pages._SiteConfig(None, None), {"notFound": None, "fileConfigs": None}
        ),
        pytest.param(
            pages._SiteConfig("abc.html", []),
            {"notFound": "abc.html", "fileConfigs": []},
        ),
        pytest.param(
            pages._SiteConfig("abc.html", [pages.FileConfig("*", "no-cache")]),
            {
                "notFound": "abc.html",
                "fileConfigs": [{"glob": "*", "options": {"cacheControl": "no-cache"}}],
            },
        ),
    ],
)
def test_pages_site_config(config: pages._SiteConfig, expected: dict[str, Any]):
    assert config.get_dict() == expected

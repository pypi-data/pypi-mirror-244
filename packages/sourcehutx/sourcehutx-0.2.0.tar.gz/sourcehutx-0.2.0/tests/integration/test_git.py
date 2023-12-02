# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio

from sourcehut.client import SRHT_SERVICE, VISIBILITY, SrhtClient
from sourcehut.services import git

from .. import vcr


@pytest_asyncio.fixture()
async def client(srht_client: SrhtClient):
    return git.GitSrhtClient(srht_client)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_git_list_repos(client: git.GitSrhtClient):
    # List repos
    repos = [
        repo async for repo in client.list_repositories("sircmpwn", max_pages=None)
    ]
    names = {repo.name for repo in repos}
    # Ensure pagination works
    assert len(repos) > 50
    # Get a list of sourcehut services
    services = {f"{key.value}.sr.ht" for key in SRHT_SERVICE}
    # Check list
    assert names & services == services
    # Ensure client is attached to each repo
    assert all(map(lambda repo: repo.client == client, repos))


@pytest.mark.asyncio
@vcr.use_cassette
async def test_git_create_repo(client: git.GitSrhtClient):
    repo = await client.create_repository("python-client-test", VISIBILITY.UNLISTED)
    try:
        whoami = await client.whoami()

        # Check expected
        expected = git.Repository(
            id=repo.id,
            client=client,
            owner=whoami,
            name="python-client-test",
            visibility=git.VISIBILITY.UNLISTED,
            description=None,
            created=repo.created,
            updated=repo.updated,
        )
        assert repo == expected

        # Check get_repository()
        gotten = await repo.get()
        assert repo == gotten

        # Check update_repository()
        newrepo = await repo.update(description="This is a description!")
        expected.description = "This is a description!"
        expected.updated = newrepo.updated
        assert newrepo == expected
    finally:
        await repo.delete()


@pytest.mark.asyncio
@vcr.use_cassette
async def test_git_upload(client: git.GitSrhtClient):
    # Get artifact contents
    contents = Path(__file__).read_bytes()
    # Create repository
    repo = await client.create_repository(
        "python-client-test-upload",
        VISIBILITY.UNLISTED,
        clone_url="https://git.sr.ht/~gotmax23/testproj",
    )
    try:
        # Upload artifact
        artifact = await repo.upload_artifact("0.0.1", "artifact.txt", contents)
        # Check artifact
        assert artifact.filename == "artifact.txt"
        # Delete artifact
        await artifact.delete()
    finally:
        await repo.delete()

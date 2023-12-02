# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
git.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime as DT
from typing import IO, TYPE_CHECKING, Optional, Union

from .._utils import check_found as _cf
from .._utils import filter_ellipsis
from .._utils import get_key as _g
from .._utils import get_locals, v_submitter
from ..client import SRHT_SERVICE, VISIBILITY, _FileUpload
from ._base import _get_user_ref, _Resource, _ServiceClient, _UserRef

if TYPE_CHECKING:
    from _typeshed import StrPath
else:
    ellipsis = type(...)


class GitSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.GIT

    async def create_repository(
        self,
        name: str,
        visibility: VISIBILITY = VISIBILITY.PUBLIC,
        description: str | None = None,
        clone_url: str | None = None,
    ) -> Repository:
        query = """
        mutation create(
          $name: String!
          $visibility: Visibility!
          $description: String,
          $cloneUrl: String
        ) {
          createRepository(
            name: $name
            visibility: $visibility
            description: $description
            cloneUrl: $cloneUrl
          ) {
            name
            visibility
            description
            id
            created
            updated
            owner {
              canonicalName
            }
          }
        }
        """
        data = await self.query(
            query,
            {
                "name": name,
                "visibility": visibility,
                "description": description,
                "cloneUrl": clone_url,
            },
        )

        return Repository(**_cf(data["createRepository"]), client=self)

    async def delete_repository(self, repoid: int | Repository) -> None:
        query = """
        mutation delete($id: Int!) {
          deleteRepository(id: $id) { id }
        }
        """
        await self.query(query, {"id": int(repoid)})

    async def get_repository(self, username: str | None, name: str) -> Repository:
        """
        Get information for a repository.

        Args:
            username:
                Username of the repository. Set to None for the current
                authenticated user.
            name:
                Name of the repository
        """
        username = await self._u(username)
        query = """
        query getRepo($username: String!, $name: String!) {
          user(username: $username) {
            repository(name: $name) {
              name
              description
              visibility
              id
              created
              updated
              owner {
                canonicalName
              }
            }
          }
        }
        """
        data = await self.query(query, {"username": username, "name": name})
        return Repository(**_g(data, "user", "repository"), client=self)

    async def update_repository(
        self,
        repoid: int | Repository,
        *,
        name: str | ellipsis = ...,
        description: str | ellipsis = ...,
        visibility: VISIBILITY | ellipsis = ...,
        readme: str | ellipsis = ...,
        HEAD: str | ellipsis = ...,
    ) -> Repository:
        inp = filter_ellipsis(
            {
                "name": name,
                "description": description,
                "visibility": visibility,
                "readme": readme,
                "HEAD": HEAD,
            }
        )
        query = """
        mutation update($id: Int!, $input: RepoInput!) {
          updateRepository(id: $id, input: $input) {
            name
            description
            visibility
            id
            created
            updated
            owner {
              canonicalName
            }
          }
        }
        """
        json = await self.query(query, variables={"id": int(repoid), "input": inp})
        return Repository(**json["updateRepository"], client=self)

    async def list_repositories(
        self, username: str | None, *, max_pages: int | None = 1
    ) -> AsyncIterator[Repository]:
        username = await self._u(username)
        query = """
        query getRepos($username: String!, $cursor: Cursor) {
          user(username: $username) {
            repositories(cursor: $cursor) {
              cursor
              results {
                name
                description
                visibility
                id
                created
                updated
                owner {
                  canonicalName
                }
              }
            }
          }
        }
        """
        async for repo in self._cursorit(
            ["user", "repositories"],
            Repository,
            query,
            max_pages,
            {"username": username},
        ):
            yield repo

    async def upload_artifact(
        self,
        repoid: int | Repository,
        revspec: str,
        filename: StrPath,
        content: str | bytes | IO[bytes],
    ) -> Artifact:
        query = """
        mutation upload($repoid: Int!, $revspec: String!, $file: Upload!) {
          uploadArtifact(repoId: $repoid, revspec: $revspec, file: $file) {
            id
            created
            filename
            checksum
            size
            url
          }
        }
        """
        variables = {"repoid": int(repoid), "revspec": revspec, "file": None}
        upload = _FileUpload(content=content, filename=filename)
        json = await self.client._query_with_upload(
            self.SERVICE, query, variables, {"file": upload}
        )
        return Artifact(**json["uploadArtifact"], client=self)

    async def delete_artifact(self, artifact: int | Artifact) -> None:
        query = """
        mutation delete($artifact: Int!) {
          deleteArtifact(id: $artifact) {
            id
          }
        }
        """
        await self.query(query, {"artifact": int(artifact)})

    async def get_user_ref(self, username: Union[str, _UserRef, None]) -> UserRef:
        return await _get_user_ref(self, UserRef, username)


class Repository(_Resource[GitSrhtClient]):
    owner: str
    name: str
    visibility: VISIBILITY
    description: Optional[str]
    created: DT
    updated: DT

    _v_owner = v_submitter("owner")

    async def delete(self) -> None:
        return await self._client.delete_repository(self)

    async def update(
        self,
        *,
        name: str | ellipsis = ...,
        description: str | ellipsis = ...,
        visibility: VISIBILITY | ellipsis = ...,
        readme: str | ellipsis = ...,
        HEAD: str | ellipsis = ...,
    ) -> Repository:
        return await self._client.update_repository(
            self,
            name=name,
            description=description,
            visibility=visibility,
            readme=readme,
            HEAD=HEAD,
        )

    async def get(self) -> Repository:
        return await self._client.get_repository(self.owner, self.name)

    async def upload_artifact(
        self,
        revspec: str,
        filename: StrPath,
        content: str | bytes | IO[bytes],
    ) -> Artifact:
        return await self._client.upload_artifact(self, **get_locals(**locals()))


class Artifact(_Resource[GitSrhtClient]):
    created: DT
    filename: str
    checksum: str
    size: int
    url: str

    async def delete(self) -> None:
        return await self._client.delete_artifact(self)


class UserRef(_UserRef, _Resource[GitSrhtClient]):
    ...


__all__ = ("GitSrhtClient", "Repository", "Artifact", "UserRef")

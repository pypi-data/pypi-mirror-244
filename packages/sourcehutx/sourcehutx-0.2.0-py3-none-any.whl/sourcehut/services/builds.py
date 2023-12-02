# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
builds.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime as DT
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from .._utils import get_locals, try_types, v_submitter
from ..client import SRHT_SERVICE, VISIBILITY
from ._base import _Resource, _ServiceClient

if TYPE_CHECKING:
    pass

_JOB_MEMBERS = """
id
created
updated
status
manifest
note
tags
visibility
image
runner
owner {
    canonicalName
}
"""
_SECRET_MEMBERS = """
id
created
uuid
name
... on SecretFile {
    path
    mode
}
"""


class BuildsSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.BUILDS

    async def submit(
        self,
        manifest: str,
        *,
        tags: list[str] | None = None,
        note: str | None = None,
        secrets: bool | None = None,
        execute: bool | None = None,
        visibility: bool | None = None,
    ):
        """
        Submit a build
        """

        inp = get_locals(**locals())
        query = (
            """
        mutation submit(
          $manifest: String!
          $tags: [String!]
          $note: String
          $secrets: Boolean
          $execute: Boolean
          $visibility: Visibility
        ) {
          submit(
            manifest: $manifest
            tags: $tags
            note: $note
            secrets: $secrets
            execute: $execute
            visibility: $visibility
          ) {
              %s
          }
        }
        """
            % _JOB_MEMBERS
        )
        json = await self.query(query, inp)
        return Job(**json["submit"], client=self)

    async def start(self, jobid: int | Job):
        """
        Start a job that was submited with `execute=False`
        """
        inp = get_locals(**locals())
        query = (
            """
        mutation start($jobid: Int!) {
          start(jobID: $jobid) {
              %s
          }
        }
        """
            % _JOB_MEMBERS
        )
        json = await self.query(query, inp)
        return Job(**json["start"], client=self)

    async def cancel(self, jobid: int | Job) -> Job:
        """
        Cancel a job
        """
        inp = get_locals(**locals())
        query = (
            """
        mutation cancel($jobid: Int!) {
          cancel(jobId: $jobid) {
              %s
          }
        }
        """
            % _JOB_MEMBERS
        )
        json = await self.query(query, inp)
        return Job(**json["cancel"], client=self)

    async def get_job(self, jobid: int | Job) -> Job:
        inp = get_locals(**locals())
        query = (
            """
        query getJob($jobid: Int!) {
          job(id: $jobid) {
              %s
          }
        }
        """
            % _JOB_MEMBERS
        )
        json = await self.query(query, inp)
        return Job(**json["job"], client=self)

    async def get_job_status(self, jobid: int | Job) -> JOB_STATUS:
        """
        Lightweight call to return the current job status
        """
        imp = get_locals(**locals())
        query = """
        query status($jobid: Int!) {
          job(id: $jobid) {
            status
          }
        }
        """
        json = await self.query(query, imp)
        return JOB_STATUS[json["job"]["status"]]

    def list_jobs(self, *, max_pages: int | None = 1) -> AsyncIterator[Job]:
        """
        Get a list of the current user's build jobs.
        This defaults to returning only first first page
        of data.
        Set `max_pages` to a higher number or `None` for unlimited.
        """
        query = (
            """
        query getJobs($cursor: Cursor) {
          jobs(cursor: $cursor) {
            cursor
            results {
                %s
            }
          }
        }
        """
            % _JOB_MEMBERS
        )
        return self._cursorit("jobs", Job, query, max_pages)

    def list_secrets(
        self, *, max_pages: int | None = 1
    ) -> AsyncIterator[SecretFile | Secret]:
        query = (
            """
        query listSecrets($cursor: Cursor) {
            secrets(cursor: $cursor) {
                cursor
                results {
                    %s
                }
            }
        } """
            % _SECRET_MEMBERS
        )
        return self._cursorit(
            "secrets", try_types(SecretFile, Secret), query, max_pages
        )


class JOB_STATUS(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"

    @property
    def succeeded(self) -> bool:
        return self == JOB_STATUS.SUCCESS

    @property
    def failed(self) -> bool:
        return self in (JOB_STATUS.FAILED, JOB_STATUS.TIMEOUT, JOB_STATUS.CANCELLED)

    @property
    def in_progress(self) -> bool:
        return self in (JOB_STATUS.PENDING, JOB_STATUS.QUEUED, JOB_STATUS.RUNNING)

    def __str__(self) -> str:
        return self.value


class Job(_Resource[BuildsSrhtClient]):
    created: DT
    updated: DT
    status: JOB_STATUS
    manifest: str
    note: Optional[str]
    tags: List[str]
    visibility: VISIBILITY
    image: str
    runner: Optional[str]
    owner: str

    _v_owner = v_submitter("owner")

    async def cancel(self) -> Job:
        """
        Cancel a job
        """
        return await self._client.cancel(self)

    async def start(self) -> Job:
        """
        Start a job that was submited with `execute=False`
        """
        return await self._client.start(self)

    async def get(self) -> Job:
        """
        Get the current state of the job
        """
        return await self._client.get_job(self)


class Secret(_Resource[BuildsSrhtClient]):
    created: DT
    uuid: str
    name: Optional[str]


class SecretFile(Secret):
    path: str
    mode: int


__all__ = ("BuildsSrhtClient", "JOB_STATUS", "Job")

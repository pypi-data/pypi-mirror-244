#!/usr/bin/env python3

# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

# Minimum Python: 3.11 due to StrEnum usage

import asyncio
from enum import StrEnum, auto
from typing import Annotated, List, Optional

import typer

from sourcehut.client import VISIBILITY, SrhtClient
from sourcehut.config import SrhtConfig
from sourcehut.services import git, lists, todo


class Service(StrEnum):
    GIT = auto()
    LISTS = auto()
    TODO = auto()


APP = typer.Typer()


@APP.command()
def main(
    *,
    name: Annotated[str, typer.Option("-n", "--name")],
    visibility: Annotated[
        Optional[VISIBILITY], typer.Option("-v", "--visibility")
    ] = None,
    services: Annotated[Optional[List[Service]], typer.Argument()] = None,
) -> None:
    async def inner():
        nonlocal services
        services = services.copy()
        if not services:
            services = list(Service)
        config = SrhtConfig.read_config()
        async with SrhtClient.from_config(config) as client:
            if Service.GIT in services:
                gitc = git.GitSrhtClient(client)
                repo = await gitc.get_repository(None, name)
                print("git:", repo.visibility)
                if visibility:
                    repo = await repo.update(visibility=visibility)
                    print("Updated git to:", repo.visibility)

            if Service.LISTS in services:
                listc = lists.ListsSrhtClient(client)
                mailing_list = await listc.get_list(None, name)
                print("lists:", mailing_list.visibility)
                if visibility:
                    mailing_list = await mailing_list.update(visibility=visibility)
                    print("Updated lists to:", mailing_list.visibility)

            if Service.TODO in services:
                todoc = todo.TodoSrhtClient(client)
                tracker = await todoc.get_tracker(None, name)
                print("todo:", tracker.visibility)
                if visibility:
                    tracker = await tracker.update(visibility=visibility)
                    print("Updated todo to:", tracker.visibility)

    asyncio.run(inner())


if __name__ == "__main__":
    APP()

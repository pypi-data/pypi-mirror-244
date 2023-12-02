# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any, TypeVar

import pytest
import pytest_asyncio
from pydantic.color import Color

from sourcehut.client import SRHT_SERVICE, VISIBILITY, SrhtClient
from sourcehut.exceptions import ResourceNotFoundError
from sourcehut.services import todo

from .. import vcr

NOT_EXISTS = "does-not-exist-123456"

if TYPE_CHECKING:
    _T = TypeVar("_T")

if sys.version_info[:2] < (3, 10):

    async def anext(it: AsyncIterator[_T]) -> _T:  # noqa: A001
        return await it.__anext__()


@pytest_asyncio.fixture()
async def client(srht_client: SrhtClient) -> todo.TodoSrhtClient:
    return todo.TodoSrhtClient(srht_client)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_whoami(client: todo.TodoSrhtClient):
    whoami = await client.whoami()
    assert whoami and isinstance(whoami, str)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_get_tracker_ref(client: todo.TodoSrhtClient):
    tracker_ref = await client.get_tracker_ref("gotmax23", "tester")
    assert tracker_ref.client
    d = tracker_ref.dict()
    assert d == {
        "id": 10353,
        "name": "tester",
        "owner": "gotmax23",
    }
    assert tracker_ref.url == "https://todo.sr.ht/~gotmax23/tester"


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_get_tracker(client: todo.TodoSrhtClient):
    tracker = await client.get_tracker("gotmax23", "tester")
    gotten = tracker.dict(exclude={"updated"})
    assert tracker.client
    expected = {
        "id": 10353,
        "name": "tester",
        "owner": "gotmax23",
        "created": tracker.created,
        "visibility": VISIBILITY.UNLISTED,
        "description": "This is a test tracker.",
    }
    assert gotten == expected
    gotten2 = await tracker.get()
    assert tracker == gotten2


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_list_trackers(client: todo.TodoSrhtClient):
    # List trackers
    trackers = [
        tracker async for tracker in client.list_trackers("sircmpwn", max_pages=None)
    ]
    names = {tracker.name for tracker in trackers}
    # Ensure pagination works
    assert len(trackers) > 50
    # Get a list of sourcehut services
    services = {f"{key.value}.sr.ht" for key in SRHT_SERVICE}
    # Check list
    assert names & services == services
    # Ensure client is attached to each tracker
    assert all(map(lambda tracker: tracker.client, trackers))


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_list_tickets(client: todo.TodoSrhtClient):
    tracker = await client.get_tracker_ref("gotmax23", "fedrq-copy")
    tickets = tracker.list_tickets()
    ticket = await anext(ticket async for ticket in tickets if ticket.id == 15)
    assert ticket == todo.Ticket(
        id=15,
        tracker=todo.TrackerRef(
            id=11641, client=client, name="fedrq-copy", owner="gotmax23"
        ),
        created=ticket.created,
        updated=ticket.updated,
        ref="~gotmax23/fedrq-copy#15",
        subject="Package fedrq for Fedora",
        body=ticket.body,
        status=todo.TICKET_STATUS.RESOLVED,
        resolution=todo.TICKET_RESOLUTION.IMPLEMENTED,
        submitter="gotmax23",
        client=client,
    )
    assert ticket.url == "https://todo.sr.ht/~gotmax23/fedrq-copy/15"


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_list_tracker_labels(client: todo.TodoSrhtClient):
    tracker = await client.get_tracker_ref("gotmax23", "fedrq-copy")
    labels = tracker.list_labels(max_pages=None)
    label = await anext(
        label async for label in labels if label.name == "3: medium-priority"
    )
    expected = todo.Label(
        id=9979,
        client=client,
        created=label.created,
        tracker=todo.TrackerRef(
            id=11641, client=client, name="fedrq-copy", owner="gotmax23"
        ),
        name="3: medium-priority",
        foregroundColor="#000",  # type: ignore[arg-type]
        backgroundColor="#ff7800",  # type: ignore[arg-type]
    )
    assert label == expected


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_create_tracker_and_label(client: todo.TodoSrhtClient):
    gotten: Any
    name = "python-source-test"
    tracker = await client.create_tracker(
        name, description="This is a test tracker", visibility=VISIBILITY.UNLISTED
    )
    try:
        gotten = await client.get_tracker(None, name)
        assert tracker == gotten

        # Ensure updating list with nothing leaves the same result
        cases: list[tuple[Any, ...]] = [
            # (),
            ("This is a test tracker",),
            ("This is a test tracker", VISIBILITY.UNLISTED),
            (..., VISIBILITY.UNLISTED),
        ]
        for data in cases:
            gotten = await tracker.update(*data)
            tracker.updated = gotten.updated
            assert gotten == tracker

        whoami = await client.whoami()
        trackerref = todo.TrackerRef(
            id=tracker.id, client=client, name=name, owner=whoami
        )
        label = await tracker.create_label("testlabel", "black", "yellow")
        # Check expected
        expected = todo.Label(
            id=label.id,
            client=client,
            created=label.created,
            tracker=trackerref,
            name="testlabel",
            backgroundColor=Color("yellow"),
            foregroundColor=Color("black"),
        )
        assert label == expected
        # Check list_labels()
        gotten = [i async for i in tracker.list_labels()]
        assert [label] == gotten
        # Check get_label()
        gotten = await label.get()
        assert label.dict() == gotten.dict()
        # Check update_label()
        newlabel = await label.update("testlabel2")
        gotten = [i async for i in tracker.list_labels()]
        assert [newlabel] == gotten
        # Check delete_label()
        await newlabel.delete()
        assert not [i async for i in tracker.list_labels()]

        ticket: todo.Ticket = await tracker.submit_ticket(
            subject="Test ticket", body="This is a test ticket!"
        )
        expected_ticket = todo.Ticket(
            id=ticket.id,
            created=ticket.created,
            updated=ticket.updated,
            tracker=trackerref,
            ref=f"~{whoami}/{ticket.tracker.name}#{ticket.id}",
            subject="Test ticket",
            body="This is a test ticket!",
            client=client,
            status=todo.TICKET_STATUS.REPORTED,
            resolution=todo.TICKET_RESOLUTION.UNRESOLVED,
            submitter=whoami,
        )
        assert ticket == expected_ticket
        gotten_ticket = await ticket.get()
        assert ticket == gotten_ticket
    finally:
        await tracker.delete()


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_subscription(client: todo.TodoSrhtClient):
    # Check subscribe_tracker()
    tracker = await client.get_tracker_ref("gotmax23", "fedrq-copy")
    subscription = await tracker.subscribe()
    # Check expected
    expected = todo.TrackerSubscription(
        id=subscription.id,
        client=client,
        tracker=tracker,
        created=subscription.created,
    )
    assert subscription == expected
    # Check get_subscription()
    gotten = await subscription.get()
    assert subscription == gotten
    # Check unsubscribe
    await subscription.unsubscribe(False)
    gotten = await tracker.get_subscription()
    assert gotten is None


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_nonexistant(client: todo.TodoSrhtClient):
    with pytest.raises(ResourceNotFoundError):
        await client.get_tracker(None, NOT_EXISTS)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_ticket_nonexistant(client: todo.TodoSrhtClient):
    with pytest.raises(ResourceNotFoundError):
        await client.get_ticket("gotmax23", "fedrq-copy", 1000)


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_default_acl(client: todo.TodoSrhtClient):
    default = dict(
        browse=True,
        submit=True,
        comment=True,
        edit=False,
        triage=False,
    )

    expected = todo.TrackerDefaultACL(client=client, **default)
    tracker_ref = await client.get_tracker_ref("gotmax23", "tester")
    gotten = await tracker_ref.get_default_acl()
    assert gotten == expected


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_default_acl_update(client: todo.TodoSrhtClient):
    default = dict(
        browse=True,
        submit=True,
        comment=True,
        edit=True,
        triage=False,
    )

    expected = todo.TrackerDefaultACL(client=client, **default)
    created = await client.create_tracker("tester-acl", visibility=VISIBILITY.UNLISTED)
    try:
        gotten = await created.update_acl(**default)
        assert gotten == expected
    finally:
        await created.delete()


@pytest.mark.asyncio
@vcr.use_cassette
async def test_todo_acls(client: todo.TodoSrhtClient):
    tracker = await client.create_tracker("test-acl2", visibility=VISIBILITY.UNLISTED)
    try:
        acls = [acl async for acl in tracker.list_acls()]
        assert not acls

        user_id = 26753  # ~gotmax23's id
        acl = await tracker.update_user_acl(user_id, True, True, True, True, True)
        expected = [
            todo.TrackerACL(
                browse=True,
                submit=True,
                comment=True,
                edit=True,
                triage=True,
                client=client,
                tracker=todo.TrackerRef(**tracker.dict()),
                id=acl.id,
                entity="gotmax23",
                created=acl.created,
            )
        ]

        acls = [a async for a in tracker.list_acls()]
        assert acls == expected

        gotten = await acl.delete()
        assert gotten == acl
    finally:
        await tracker.delete()

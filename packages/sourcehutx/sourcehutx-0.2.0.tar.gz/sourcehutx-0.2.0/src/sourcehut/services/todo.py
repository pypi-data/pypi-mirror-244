# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# ruff: noqa: ARG002

"""
todo.sr.ht API
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from datetime import datetime as DT
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union, overload

from pydantic import BaseModel, Field
from pydantic.color import Color

from .._utils import check_found as _cf
from .._utils import filter_ellipsis
from .._utils import get_key as _g
from .._utils import get_locals, v_client, v_submitter
from ..client import SRHT_SERVICE, VISIBILITY
from ._base import _BaseResource, _get_user_ref, _Resource, _ServiceClient, _UserRef

if TYPE_CHECKING:
    pass
else:
    ellipsis = type(...)

_TRACKER_REF_MEMBERS = """
id
name
owner {
    canonicalName
}
"""

_TRACKER_MEMBERS = """
id
created
updated
name
description
visibility
"""

_ACL_BASE_MEMBERS = """
browse
submit
comment
edit
triage
"""

_ACL_MEMBERS = (
    _ACL_BASE_MEMBERS
    + """
id
created
tracker {
    %s
}
entity {
    canonicalName
}
"""
    % _TRACKER_REF_MEMBERS
)


class TodoSrhtClient(_ServiceClient):
    SERVICE = SRHT_SERVICE.TODO

    async def create_tracker(
        self,
        name: str,
        description: str | None = None,
        visibility: VISIBILITY = VISIBILITY.PUBLIC,
    ) -> Tracker:
        inp = get_locals(**locals())
        query = (
            """
        mutation create(
          $name: String!
          $description: String
          $visibility: Visibility!
        ) {
          createTracker(
            name: $name
            description: $description
            visibility: $visibility
          ) {
              %s
          }
        }
        """
            % _TRACKER_MEMBERS
        )
        json = await self.query(query, inp)
        whoami = await self.whoami()
        return Tracker(**json["createTracker"], client=self, owner=whoami)

    async def update_tracker(
        self,
        trackerid: int | TrackerRef,
        description: str | None | ellipsis = ...,
        visibility: VISIBILITY | ellipsis = ...,
    ) -> Tracker:
        inp = filter_ellipsis(get_locals(**locals()))
        trackerid = inp.pop("trackerid")
        query = (
            """
        mutation updateTracker($trackerid: Int!, $inp: TrackerInput!) {
            updateTracker(id: $trackerid, input: $inp) {
                %s
                owner {
                    canonicalName
                }
            }
        }
        """
            % _TRACKER_MEMBERS
        )
        data = await self.query(query, {"inp": inp, "trackerid": trackerid})
        return Tracker(**_g(data, "updateTracker"), client=self)

    async def get_tracker_ref(self, username: str, name: str) -> TrackerRef:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = """
        query get(
          $username: String!
          $name: String!
        ) {
          user(username: $username) {
            tracker(name: $name) {
              name
              id
            }
          }
        }
        """
        json = await self.query(query, inp)
        return TrackerRef(**_g(json, "user", "tracker"), owner=username, client=self)

    async def get_tracker(self, username: str | None, name: str) -> Tracker:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = (
            """
        query get(
          $username: String!
          $name: String!
        ) {
          user(username: $username) {
            tracker(name: $name) {
                %s
            }
          }
        }
        """
            % _TRACKER_MEMBERS
        )
        json = await self.query(query, inp)
        return Tracker(**_g(json, "user", "tracker"), client=self, owner=username)

    async def list_trackers(
        self, username: str | None = None, *, max_pages: int | None = 1
    ) -> AsyncIterator[Tracker]:
        username = await self._u(username)
        query = (
            """
        query list(
          $username: String!
          $cursor: Cursor
        ) {
          user(username: $username) {
            trackers(cursor: $cursor) {
              cursor
              results {
                  %s
              }
            }
          }
        }
        """
            % _TRACKER_MEMBERS
        )
        it = self._cursorit(
            ["user", "trackers"],
            Tracker,
            query,
            max_pages,
            {"username": username},
            {"owner": username},
        )
        async for i in it:
            yield i

    async def get_tracker_default_acl(
        self, username: str | None, tracker: str
    ) -> TrackerDefaultACL:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = (
            """
        query getTrackerDefaultAcl($username: String!, $tracker: String!) {
            user(username: $username) {
                tracker(name: $tracker) {
                    defaultACL {
                        %s
                    }
                }
            }
        }
        """
            % _ACL_BASE_MEMBERS
        )

        data = await self.query(query, inp)
        return TrackerDefaultACL(
            **_g(data, "user", "tracker", "defaultACL"), client=self
        )

    async def update_tracker_acl(
        self,
        tracker_id: TrackerRef | int,
        browse: bool,
        submit: bool,
        comment: bool,
        edit: bool,
        triage: bool,
    ) -> TrackerDefaultACL:
        inp = get_locals(**locals())
        tracker_idn: int = inp.pop("tracker_id")
        query = (
            """
        mutation updateTrackerACL($tracker_id: Int!, $inp: ACLInput!) {
            updateTrackerACL(trackerId: $tracker_id, input: $inp) {
                %s
            }
        }
        """
            % _ACL_BASE_MEMBERS
        )
        data = await self.query(query, {"inp": inp, "tracker_id": tracker_idn})
        return TrackerDefaultACL(**_cf(data["updateTrackerACL"]), client=self)

    async def list_tracker_acls(
        self, username: str | None, tracker: str, *, max_pages: int | None = 1
    ) -> AsyncIterator[TrackerACL]:
        username = await self._u(username)
        query = (
            """
        query listTrackerAcls($username: String!, $tracker: String!, $cursor: Cursor) {
            user(username: $username) {
                tracker(name: $tracker) {
                    acls(cursor: $cursor) {
                        cursor
                        results {
                            %s
                        }
                    }
                }
            }
        }
        """
            % _ACL_MEMBERS
        )
        async for i in self._cursorit(
            ["user", "tracker", "acls"],
            TrackerACL,
            query,
            max_pages,
            {"username": username, "tracker": tracker},
        ):
            yield i

    async def update_user_acl(
        self,
        tracker_id: int | TrackerRef,
        user_id: int,
        browse: bool,
        submit: bool,
        comment: bool,
        edit: bool,
        triage: bool,
    ) -> TrackerACL:
        inp = get_locals(**locals())
        variables = {
            "tracker_id": inp.pop("tracker_id"),
            "user_id": inp.pop("user_id"),
            "inp": inp,
        }
        query = (
            """
        mutation updateUserAcl($inp: ACLInput!, $tracker_id: Int!, $user_id: Int!) {
            updateUserACL(trackerId: $tracker_id, userId: $user_id, input: $inp) {
                %s
            }
        }
        """
            % _ACL_MEMBERS
        )
        data = await self.query(query, variables)
        return TrackerACL(**data["updateUserACL"], client=self)

    async def delete_acl(self, acl_id: int | TrackerACLRef) -> TrackerACL:
        inp = get_locals(**locals())
        query = (
            """
        mutation deleteACL($acl_id: Int!) {
            deleteACL(id: $acl_id) {
                %s
            }
        }
        """
            % _ACL_MEMBERS
        )
        data = await self.query(query, inp)
        return TrackerACL(**_cf(data["deleteACL"]), client=self)

    @overload
    @staticmethod
    def _validate_color(*colors: str | Color) -> Iterator[str]:
        ...

    @overload
    @staticmethod
    def _validate_color(*colors: str | Color | ellipsis) -> Iterator[str | ellipsis]:
        ...

    @staticmethod
    def _validate_color(*colors):
        for color in colors:
            if color is ...:
                yield color
                continue
            if isinstance(color, str):
                color = Color(color)
            r, g, b = color.as_rgb_tuple()
            c = f"#{r:02x}{g:02x}{b:02x}"
            yield c

    async def create_label(
        self,
        tracker: int | TrackerRef,
        name: str,
        foreground_color: str | Color,
        background_color: str | Color,
    ):
        tracker = int(tracker)
        foreground_color, background_color = self._validate_color(
            foreground_color, background_color
        )
        inp = get_locals(**locals())
        query = """
        mutation createLabel(
          $tracker: Int!
          $name: String!
          $foreground_color: String!
          $background_color: String!
        ) {
            createLabel(
              trackerId: $tracker
              name: $name
              foregroundColor: $foreground_color
              backgroundColor: $background_color
            ) {
              id
              created
              name
              backgroundColor
              foregroundColor
              tracker {
                name
                id
                owner {
                  canonicalName
                }
              }
          }
        }
        """
        json = await self.query(query, inp)
        return Label(**_cf(json["createLabel"]), client=self)

    async def delete_label(self, label: Label | int) -> None:
        label = int(label)
        query = """
        mutation deleteLabel(
          $label: Int!
        ) {
          deleteLabel(id: $label) {
            id
            tracker {
              name
              id
              owner {
                canonicalName
              }
            }
          }
        }
        """
        await self.query(query, {"label": label})

    async def update_label(
        self,
        label: int | Label,
        name: str | ellipsis = ...,
        foreground_color: Color | str | ellipsis = ...,
        background_color: Color | str | ellipsis = ...,
    ) -> Label:
        label = int(label)
        foreground_color, background_color = self._validate_color(
            foreground_color, background_color
        )
        inp = filter_ellipsis(
            {
                "name": name,
                "foreground_color": foreground_color,
                "background_color": background_color,
            }
        )
        query = """
        mutation update($label: Int!, $input: UpdateLabelInput!) {
          updateLabel(id: $label, input: $input) {
            id
            name
            created
            foregroundColor
            backgroundColor
            tracker {
              name
              id
              owner {
                canonicalName
              }
            }
          }
        }
        """
        json = await self.query(query, {"label": label, "input": inp})
        label = Label(**json["updateLabel"], client=self)
        return label

    async def subscribe_tracker(self, tracker: int | TrackerRef) -> TrackerSubscription:
        tracker = int(tracker)
        query = """
        mutation subscribe($tracker: Int!) {
          trackerSubscribe(trackerId: $tracker) {
            id
            created
            tracker {
              name
              id
              owner {
                canonicalName
              }
            }
          }
        }
        """
        json = await self.query(query, {"tracker": tracker})
        return TrackerSubscription(**json["trackerSubscribe"], client=self)

    async def unsubscribe_tracker(
        self, tracker: int | TrackerRef, tickets: bool
    ) -> TrackerSubscription:
        tracker = int(tracker)
        inp = get_locals(**locals())
        query = """
        mutation unsubscribe($tracker: Int!, $tickets: Boolean!) {
          trackerUnsubscribe(trackerId: $tracker, tickets: $tickets) {
            id
            created
            tracker {
              name
              id
              owner {
                canonicalName
              }
            }
          }
        }
        """
        json = await self.query(query, inp)
        return TrackerSubscription(**json["trackerUnsubscribe"], client=self)

    async def get_subscription(
        self, username: str | None, name: str
    ) -> TrackerSubscription | None:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = """
        query getSubscription($username: String!, $name: String!) {
          user(username: $username) {
            tracker(name: $name) {
              subscription {
                id
                created
                tracker {
                  id
                  name
                  owner {
                    canonicalName
                  }
                }
              }
            }
          }
        }
        """
        json = await self.query(query, inp)
        data = _g(json, "user", "tracker")["subscription"]
        if data is None:
            return data
        return TrackerSubscription(**data, client=self)

    async def list_tickets(
        self, username: str | None, name: str, *, max_pages: int | None = 1
    ) -> AsyncIterator[Ticket]:
        username = await self._u(username)
        inp = {"username": username, "name": name}
        query = """
        query($username: String!, $name: String!, $cursor: Cursor) {
          user(username: $username) {
            tracker(name: $name) {
              tickets(cursor: $cursor) {
                cursor
                results {
                  id
                  created
                  updated
                  ref
                  subject
                  body
                  status
                  resolution
                  submitter {
                    canonicalName
                  }
                  tracker {
                    id
                    name
                    owner {
                      canonicalName
                    }
                  }
                }
              }
            }
          }
        }
        """
        async for ticket in self._cursorit(
            ["user", "tracker", "tickets"],
            Ticket,
            query,
            max_pages,
            inp,
        ):
            yield ticket

    async def submit_ticket(
        self, tracker: int | TrackerRef, subject: str, body: str | None
    ) -> Ticket:
        tracker = int(tracker)
        inp = {"subject": subject, "body": body}
        query = """
        mutation submit($tracker: Int!, $input: SubmitTicketInput!) {
          submitTicket(trackerId: $tracker, input: $input) {
            id
            created
            updated
            ref
            subject
            body
            status
            resolution
            submitter {
              canonicalName
            }
            tracker {
              name
              id
              owner {
                canonicalName
              }
            }
          }
        }
        """
        json = await self.query(query, {"tracker": tracker, "input": inp})
        ticket = Ticket(**json["submitTicket"], client=self)
        return ticket

    async def get_ticket(
        self, username: str | None, name: str, ticket: int | TicketRef
    ) -> Ticket:
        username = await self._u(username)
        ticket = int(ticket)
        inp = get_locals(**locals())
        query = """
        query getTicket($username: String!, $name: String!, $ticket: Int!){
          user(username: $username) {
            tracker(name: $name) {
              ticket(id: $ticket) {
                id
                created
                updated
                ref
                subject
                body
                status
                resolution
                submitter {
                  canonicalName
                }
                tracker {
                  name
                  id
                  owner {
                    canonicalName
                  }
                }
              }
            }
          }
        }
        """
        json = await self.query(query, inp)
        return Ticket(**_g(json, "user", "tracker", "ticket"), client=self)

    async def delete_tracker(self, tracker: int | TrackerRef) -> None:
        tracker = int(tracker)
        inp = get_locals(**locals())
        query = """
        mutation delete($tracker: Int!) {
          deleteTracker(id: $tracker) {
            id
          }
        }
        """
        await self.query(query, inp)

    async def get_label(self, username: str | None, name: str, label: str) -> Label:
        username = await self._u(username)
        inp = get_locals(**locals())
        query = """
        query getLabel($username: String!, $name: String!, $label: String!) {
          user(username: $username) {
            tracker(name: $name) {
              id
              label(name: $label) {
                id
                created
                name
                foregroundColor
                backgroundColor
              }
            }
          }
        }
        """
        json = await self.query(query, inp)
        tracker = _g(json, "user", "tracker")
        tracker_ref = TrackerRef(
            owner=username, name=name, id=tracker["id"], client=self
        )
        return Label(**_cf(tracker["label"]), tracker=tracker_ref)

    async def get_user_ref(self, username: Union[str, _UserRef, None]) -> UserRef:
        return await _get_user_ref(self, UserRef, username)


class TrackerRef(_Resource[TodoSrhtClient]):
    name: str
    owner: str

    _v_tracker = v_submitter("owner")

    async def get(self) -> Tracker:
        return await self._client.get_tracker(self.owner, self.name)

    async def update(
        self,
        description: str | None | ellipsis = ...,
        visibility: VISIBILITY | ellipsis = ...,
    ) -> Tracker:
        return await self._client.update_tracker(self, description, visibility)

    async def create_label(
        self, name: str, foreground_color: str | Color, background_color: str | Color
    ) -> Label:
        return await self._client.create_label(
            self, name, foreground_color, background_color
        )

    async def subscribe(self) -> TrackerSubscription:
        return await self._client.subscribe_tracker(self)

    async def unsubscribe(self, tickets: bool) -> TrackerSubscription:
        return await self._client.unsubscribe_tracker(self, tickets)

    async def get_subscription(self) -> TrackerSubscription | None:
        return await self._client.get_subscription(self.owner, self.name)

    def list_tickets(self, *, max_pages: int | None = 1) -> AsyncIterator[Ticket]:
        return self._client.list_tickets(self.owner, self.name, max_pages=max_pages)

    async def submit_ticket(self, subject: str, body: str | None) -> Ticket:
        return await self._client.submit_ticket(self, subject, body)

    @property
    def url(self) -> str:
        protocol = self._client.client.protocol
        baseurl = self._client.client.baseurl
        return f"{protocol}todo.{baseurl}/~{self.owner}/{self.name}"

    async def delete(self) -> None:
        return await self._client.delete_tracker(self)

    def list_labels(self, *, max_pages: int | None = 1) -> AsyncIterator[Label]:
        inp = {"username": self.owner, "name": self.name}
        query = """
        query($username: String!, $name: String!, $cursor: Cursor) {
          user(username: $username) {
            tracker(name: $name) {
              labels(cursor: $cursor) {
                cursor
                results {
                  name
                  id
                  backgroundColor
                  foregroundColor
                  created
                }
              }
            }
          }
        }
        """
        return self._client._cursorit(
            ["user", "tracker", "labels"],
            Label,
            query,
            max_pages,
            inp,
            {"tracker": TrackerRef(**self.dict())},
        )

    async def get_label(self, name: str) -> Label:
        return await self._client.get_label(self.owner, self.name, name)

    async def get_ticket(self, ticket: int | TicketRef) -> Ticket:
        return await self._client.get_ticket(self.owner, self.name, ticket)

    async def get_default_acl(self) -> TrackerDefaultACL:
        return await self._client.get_tracker_default_acl(self.owner, self.name)

    async def update_acl(
        self,
        browse: bool,
        submit: bool,
        comment: bool,
        edit: bool,
        triage: bool,
    ) -> TrackerDefaultACL:
        return await self._client.update_tracker_acl(self, **get_locals(**locals()))

    def list_acls(self, *, max_pages: int | None = 1) -> AsyncIterator[TrackerACL]:
        return self._client.list_tracker_acls(
            self.owner, self.name, max_pages=max_pages
        )

    async def update_user_acl(
        self,
        user_id: int,
        browse: bool,
        submit: bool,
        comment: bool,
        edit: bool,
        triage: bool,
    ) -> TrackerACL:
        return await self._client.update_user_acl(
            tracker_id=self, **get_locals(**locals())
        )


class Tracker(TrackerRef):
    created: DT
    updated: DT
    description: Optional[str]
    visibility: VISIBILITY


class TICKET_STATUS(str, Enum):
    REPORTED = "REPORTED"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class TICKET_RESOLUTION(str, Enum):
    UNRESOLVED = "UNRESOLVED"
    CLOSED = "CLOSED"
    FIXED = "FIXED"
    IMPLEMENTED = "IMPLEMENTED"
    WONT_FIX = "WONT_FIX"
    BY_DESIGN = "BY_DESIGN"
    INVALID = "INVALID"
    DUPLICATE = "DUPLICATE"
    NOT_OUR_BUG = "NOT_OUR_BUG"


class TicketRef(_Resource[TodoSrhtClient]):
    tracker: TrackerRef
    _v_client = v_client("tracker")

    async def get(self) -> Ticket:
        return await self.tracker.get_ticket(self)

    # def list_comments(self) -> AsyncIterator[Ticket]:
    #     pass


class Ticket(TicketRef):
    created: DT
    updated: DT
    ref: str
    subject: str
    body: Optional[str]
    status: TICKET_STATUS
    resolution: Optional[TICKET_RESOLUTION]
    tracker: TrackerRef
    submitter: str
    # TODO: assignees

    _v_submitter = v_submitter("submitter")
    _v_tracker = v_client("tracker")

    @property
    def url(self) -> str:
        return f"{self.tracker.url}/{self.id}"


class Comment:
    text: str
    author: str
    _v_submitter = v_submitter("author")


class Label(_Resource[TodoSrhtClient]):
    created: DT
    tracker: TrackerRef
    name: str
    foreground_color: Color = Field(alias="foregroundColor")
    background_color: Color = Field(alias="backgroundColor")
    _v_client = v_client("tracker")

    async def delete(self) -> None:
        return await self._client.delete_label(self)

    async def get(self) -> Label:
        return await self.tracker.get_label(self.name)

    async def update(
        self,
        name: str | ellipsis = ...,
        foreground_color: Color | str | ellipsis = ...,
        background_color: Color | str | ellipsis = ...,
    ) -> Label:
        inp = get_locals(label=self, **locals())
        return await self._client.update_label(**inp)


class TrackerSubscription(_Resource[TodoSrhtClient]):
    created: DT
    tracker: TrackerRef
    _v_client = v_client("tracker")

    async def unsubscribe(self, tickets: bool) -> None:
        await self.tracker.unsubscribe(tickets)

    async def get(self) -> TrackerSubscription | None:
        return await self.tracker.get_subscription()


class TrackerACLBase(BaseModel):
    browse: bool
    submit: bool
    comment: bool
    edit: bool
    triage: bool


class TrackerDefaultACL(TrackerACLBase, _BaseResource[TodoSrhtClient]):
    ...


class TrackerACLRef(_Resource[TodoSrhtClient]):
    tracker: TrackerRef
    entity: str

    _v_client = v_client("tracker")
    _v_entity = v_submitter("entity")

    async def delete(self) -> TrackerACL:
        return await self._client.delete_acl(self)


class TrackerACL(TrackerACLRef, TrackerACLBase):
    created: DT


class UserRef(_UserRef, _Resource[TodoSrhtClient]):
    ...


__all__ = (
    "TodoSrhtClient",
    "TrackerRef",
    "Tracker",
    "TICKET_STATUS",
    "TICKET_RESOLUTION",
    "TicketRef",
    "Ticket",
    "Comment",
    "Label",
    "TrackerSubscription",
    "TrackerDefaultACL",
    "TrackerACLRef",
    "TrackerACL",
    "UserRef",
)

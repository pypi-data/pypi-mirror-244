# bles --- Event Sourcing library
# Copyright © 2021-2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum as Enumeration
from enum import auto
from typing import Any, Iterator, Optional


def camel_to_snake(string: str) -> str:
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


@dataclass
class Event:
    """Something that happened."""

    stream_id: str
    version: int  # Must be unique in a given stream
    name: str
    data: dict[str, Any]
    position: Optional[int] = None
    recorded_at: Optional[datetime] = None


class EventStore(ABC):
    """Repository for events."""

    @abstractmethod
    def record(self, events: list[Event]) -> None:
        ...

    @abstractmethod
    def for_stream(self, name: str) -> "EventStore":
        ...

    @abstractmethod
    def read(self, start: int = 0, follow: bool = False) -> Iterator[Event]:
        ...

    @abstractmethod
    def last(self) -> Optional[Event]:
        ...


class Projection(ABC):
    """A "point of view" on the data.

    They contain methods to write data to the chosen storage
    (SQL, no-SQL, in-memory…) and methods to query the data back.
    """

    ...


class ProjectorTypes(Enumeration):
    RUN_FROM_BEGINNING = auto()
    """Plays all the events during the boot phase then keep on playing new ones.

    Used, for instance, to populate a projection.
    """

    RUN_FROM_NOW = auto()
    """Skips the boot phase then play all the events as usual.

    Used, for instance, to send email notifications from now on.
    """

    RUN_ONCE = auto()
    """Plays existing events during the boot phase then does not play anymore.

    Used, for instance, to add new events to the store based on the old ones.
    """


class Projector(ABC):
    """Parses event's data and calls the proper projection method.

    Projectors exist in different types, that implement `boot` and `play` differently.
    """

    NAME: str
    TYPE: ProjectorTypes
    PREFIX: str = "when"

    class EventHandlerCrashed(Exception):
        def __init__(self, method_name: str, exception: Exception) -> None:
            super().__init__(
                "Event handler raised an exception! "
                f"[handler: {method_name}, "
                f"exception: {exception.__class__.__name__}, "
                f"message: {exception}]"
            )

    def process(self, event: Event) -> None:
        logger = logging.getLogger(f"Projector/{self.NAME}")
        if not event.recorded_at:
            raise RuntimeError("No event does not contain `recorded_at`!")

        method_name = f"{self.PREFIX}_{camel_to_snake(event.name)}"
        method = getattr(self, method_name, None)
        if method:
            logger.info(
                f"Processing event. [projector={self.__class__.__name__}, "
                f"stream_id={event.stream_id}, version={event.version}, "
                f"name={event.name}]"
            )
            logger.debug(f"Data = {event.data}")
            try:
                method(event.recorded_at, event.data)
            except Exception as exc:
                raise Projector.EventHandlerCrashed(method_name, exc)
        else:
            logger.debug(f"No method to handle event. [name={event.name}]")


class ProjectorStatuses(Enumeration):
    # NEW
    # Never booted nor played. Never to be actually used.

    STALLED = auto()
    "Ready to be booted."

    OK = auto()
    "Successfully played."

    BROKEN = auto()
    "Crashed while being played."

    RETIRED = auto()
    "Never to be booted nor played again."


class Ledger(ABC):
    """Keeps track of a projector's lifecycle.

    From <https://barryosull.com/blog/managing-projectors-is-harder-than-you-think/>.
    """

    class UnknownProjector(Exception):
        def __init__(self, name: str) -> None:
            super().__init__(f"Unknown projector [name={name}]")

    class ProjectorAlreadyRegistered(Exception):
        def __init__(self, name: str) -> None:
            super().__init__(f"Projector already registered [name={name}]")

    @abstractmethod
    def status(self) -> list[tuple[str, ProjectorStatuses, int]]:
        ...

    @abstractmethod
    def knows(self, name: str) -> bool:
        ...

    @abstractmethod
    def register(self, name: str) -> None:
        ...

    @abstractmethod
    def forget(self, name: str) -> None:
        ...

    @abstractmethod
    def position(self, name: str) -> int:
        ...

    @abstractmethod
    def update_position(self, name: str, position: int) -> None:
        ...

    @abstractmethod
    def find(self, status: Optional[ProjectorStatuses] = None) -> list[str]:
        ...

    @abstractmethod
    def mark_as(self, name: str, status: ProjectorStatuses) -> None:
        ...


class Projectionist:
    """Boots and runs all the registered projectors."""

    def __init__(self, store: EventStore, ledger: Ledger) -> None:
        self.__logger = logging.getLogger("Projectionist")
        self.__store = store
        self.__ledger = ledger
        self.__projectors: dict[str, Projector] = {}
        self.__last_seen_position: int = 0

    def register(self, projector: Projector) -> None:
        self.__projectors[projector.NAME] = projector

    def boot(self) -> None:
        self.__mark_new_projectors_as_stalled()
        self.__mark_broken_as_stalled()
        self.__boot_stalled_projectors()

    def __mark_new_projectors_as_stalled(self) -> None:
        for n, p in self.__projectors.items():
            if not self.__ledger.knows(n):
                self.__ledger.register(n)

    def __mark_broken_as_stalled(self) -> None:
        for name in self.__ledger.find(ProjectorStatuses.BROKEN):
            self.__ledger.mark_as(name, ProjectorStatuses.STALLED)

    def __boot_stalled_projectors(self) -> None:
        for name in self.__ledger.find(ProjectorStatuses.STALLED):
            self.__boot_projector(name)

    def __boot_projector(self, name: str) -> None:
        try:
            projector = self.__projectors[name]
            current_position = self.__ledger.position(name)
            for e in self.__store.read(start=current_position + 1):
                if self.__is_bootable(projector):
                    projector.process(e)
                assert e.position is not None, "Events read MUST have a position!"
                current_position = e.position
            if projector.TYPE == ProjectorTypes.RUN_ONCE:
                self.__ledger.mark_as(name, ProjectorStatuses.RETIRED)
            else:
                self.__ledger.mark_as(name, ProjectorStatuses.OK)
            self.__ledger.update_position(name, current_position)
        except Exception as exc:
            self.__ledger.mark_as(name, ProjectorStatuses.BROKEN)
            self.__logger.error(
                "Error while booting projector! "
                f"[projector={name}, error={exc.__class__.__name__}, "
                f"message={exc}]"
            )
            self.__logger.debug(exc)

    def __is_bootable(self, projector: Projector) -> bool:
        return projector.TYPE in [
            ProjectorTypes.RUN_FROM_BEGINNING,
            ProjectorTypes.RUN_ONCE,
        ]

    def play(self, follow: bool = False) -> None:
        list_projectors = self.__ledger.find(ProjectorStatuses.OK)
        positions = [self.__ledger.position(n) for n in list_projectors]
        current_position = min(positions) if positions else 0
        for e in self.__store.read(start=current_position + 1, follow=False):
            assert e.position is not None, "Events read MUST have a position!"
            current_position = e.position
            for name in self.__ledger.find(ProjectorStatuses.OK):
                if e.position <= self.__ledger.position(name):
                    continue
                if (p := self.__projectors.get(name)) and self.__is_playable(p):
                    self.__process_event(p, e)

        if not follow:
            return

        for e in self.__store.read(start=current_position + 1, follow=True):
            for name in self.__ledger.find(ProjectorStatuses.OK):
                if (p := self.__projectors.get(name)) and self.__is_playable(p):
                    self.__process_event(p, e)

    def __process_event(self, projector: Projector, event: Event) -> None:
        assert event.position is not None, "Events read MUST have a position!"
        try:
            projector.process(event)
            self.__ledger.update_position(projector.NAME, event.position)
        except Exception as exc:
            self.__ledger.mark_as(projector.NAME, ProjectorStatuses.BROKEN)
            self.__logger.error(
                "Error while playing projector! "
                f"[projector={projector.NAME}, error={exc.__class__.__name__}, "
                f"message={exc}]"
            )

    def __is_playable(self, projector: Projector) -> bool:
        return projector.TYPE in [
            ProjectorTypes.RUN_FROM_BEGINNING,
            ProjectorTypes.RUN_FROM_NOW,
        ]

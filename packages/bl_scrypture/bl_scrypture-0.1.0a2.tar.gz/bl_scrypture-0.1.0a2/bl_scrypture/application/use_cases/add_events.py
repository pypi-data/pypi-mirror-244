# Scrypture --- An event store
# Copyright © 2023 Bioneland
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
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from bles import Event, EventStore
from bles.utils import event_from_string

from bl_scrypture.domain import IntegrityError, Notifier


class Presenter(ABC):
    @abstractmethod
    def no_events(self) -> None:
        ...

    @abstractmethod
    def bad_events(self) -> None:
        ...

    @abstractmethod
    def events_on_different_streams(self) -> None:
        ...

    @abstractmethod
    def events_not_consecutive(self, expected: int, actual: int) -> None:
        ...

    @abstractmethod
    def events_not_compatible(self) -> None:
        ...

    @abstractmethod
    def unexpected_error(self) -> None:
        ...

    @abstractmethod
    def events_recorded(self) -> None:
        ...


@dataclass
class Interactor:
    presenter: Presenter
    store: EventStore
    notifier: Notifier

    def execute(self, strings: list[str]) -> None:
        try:
            events = [event_from_string(s) for s in strings]
        except KeyError:
            return self.presenter.bad_events()

        if not events:
            return self.presenter.no_events()

        expected_stream = events[0].stream_id
        if last := self.store.for_stream(expected_stream).last():
            expected_version = last.version + 1
        else:
            expected_version = 1

        if events[0].version != expected_version:
            return self.presenter.events_not_compatible()

        if len(events) > 1:
            for e in events:
                if expected_stream != e.stream_id:
                    return self.presenter.events_on_different_streams()

                if expected_version != e.version:
                    return self.presenter.events_not_consecutive(
                        expected_version, e.version
                    )
                expected_version += 1

        try:
            self.store.record(events)
        except IntegrityError as exc:
            logging.exception(exc)
            return self.presenter.events_not_compatible()
        except Exception as exc:
            logging.exception(exc)
            return self.presenter.unexpected_error()

        self.notifier.events_added()
        self.presenter.events_recorded()


def event_from_dict(data: dict[str, Any]) -> Event:
    recorded_at: Optional[datetime] = None
    if isoformat := data.get("recorded_at"):
        recorded_at = datetime.fromisoformat(isoformat)
        recorded_at = recorded_at.replace(tzinfo=timezone.utc)

    position: Optional[int] = None
    if value := data.get("position"):
        position = int(value)

    return Event(
        recorded_at=recorded_at,
        stream_id=data["stream_id"],
        version=data["version"],
        name=data["name"],
        data=data["data"],
        position=position,
    )

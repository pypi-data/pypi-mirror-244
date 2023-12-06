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

from typing import Optional

from blessql.events import EventStore
from flask import g
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bl_scrypture.domain import Notifier as NotifierInterface
from bl_scrypture.infrastructure.redis import Notifier
from bl_scrypture.infrastructure.settings import WsgiSettings

__SETTINGS: Optional[WsgiSettings] = None


class FakeNotifier(NotifierInterface):
    def __bool__(self) -> bool:
        return False

    def events_added(self) -> None:
        pass

    def something_happened(self) -> bool:
        return False


def define_settings(settings: WsgiSettings) -> None:
    global __SETTINGS
    __SETTINGS = settings


def get_settings() -> WsgiSettings:
    if not __SETTINGS:
        raise RuntimeError("You must define the settings!")
    return __SETTINGS


def is_read_only() -> bool:
    return get_settings().READ_ONLY


def get_session() -> Session:
    if "session" not in g:
        engine = create_engine(get_settings().DSN)
        g.setdefault("session", sessionmaker(bind=engine)())

    return g.session  # type: ignore[no-any-return]


def close_session(exception: Optional[BaseException]) -> None:
    if session := g.pop("session", None):
        if exception:
            session.rollback()
        else:
            session.commit()
        session.close()


def get_store() -> EventStore:
    return EventStore(get_session())


def get_notifier() -> NotifierInterface:
    s = get_settings()

    if not s.REDIS:
        return FakeNotifier()

    if "redis" not in g:
        g.setdefault("redis", Redis(host=s.REDIS.HOST, port=s.REDIS.PORT, db=s.REDIS.DB))

    return Notifier(g.redis)

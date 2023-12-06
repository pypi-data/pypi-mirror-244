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

from redis import Redis

from bl_scrypture.domain import Notifier as NotifierInterface


class Notifier(NotifierInterface):
    def __init__(self, redis: "Redis") -> None:  # type: ignore[type-arg]
        self.__redis = redis
        self.__pubsub = redis.pubsub()
        self.__pubsub.subscribe("events")

    def events_added(self) -> None:
        self.__redis.publish("events", "event_added")

    def something_happened(self) -> bool:
        return bool(self.__pubsub.get_message())

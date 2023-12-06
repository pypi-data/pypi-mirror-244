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

from dataclasses import dataclass
from typing import Optional

import bl_seth


@dataclass(frozen=True)
class RedisSettings(bl_seth.Settings):
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 0


@dataclass(frozen=True)
class CliSettings(bl_seth.Settings):
    DSN: str


@dataclass(frozen=True)
class WsgiSettings(bl_seth.Settings):
    DSN: str

    READ_ONLY: bool = False

    REDIS: Optional[RedisSettings] = None

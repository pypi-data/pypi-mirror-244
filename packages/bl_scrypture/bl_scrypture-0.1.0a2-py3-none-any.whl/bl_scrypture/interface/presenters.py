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

from bl_scrypture.application.use_cases import add_events


class AddEvents(add_events.Presenter):
    def __init__(self) -> None:
        self.response = "Something weird happened!", 500

    def no_events(self) -> None:
        self.response = "No events given!", 400

    def bad_events(self) -> None:
        self.response = "Cannot instanciate events from data!", 400

    def events_on_different_streams(self) -> None:
        self.response = "The events must be on the same stream!", 400

    def events_not_consecutive(self, expected: int, actual: int) -> None:
        self.response = (
            "The events must be consecutive! " f"[expected={expected}, actual={actual}]"
        ), 400

    def events_not_compatible(self) -> None:
        self.response = (
            "Events are not compatible with the current state of the stream!",
            409,
        )

    def unexpected_error(self) -> None:
        self.response = "Something unexpected happened!", 500

    def events_recorded(self) -> None:
        self.response = "Events successfully recorded!", 201

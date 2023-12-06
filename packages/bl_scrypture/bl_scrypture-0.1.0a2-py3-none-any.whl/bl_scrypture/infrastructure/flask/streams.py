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

import time
from typing import Any, Iterator, Optional

from bles.utils import event_to_string
from flask import Blueprint, request, stream_with_context
from werkzeug.exceptions import NotImplemented as HttpNotImplemented

from bl_scrypture.application.use_cases import add_events
from bl_scrypture.infrastructure.flask import services
from bl_scrypture.interface import controllers, presenters

blueprint = Blueprint("streams", __name__)


@blueprint.post("/")
def add() -> Any:
    if services.is_read_only():
        return "Event store is read only!", 403

    presenter = presenters.AddEvents()
    interactor = add_events.Interactor(
        presenter, services.get_store(), services.get_notifier()
    )
    controller = controllers.AddEvents(request.get_data())
    controller.call(interactor)

    return presenter.response


@blueprint.get("/", defaults={"stream": "*"})
@blueprint.get("/<stream>")
def read(stream: str) -> Any:
    start: Optional[int] = None
    if "start" in request.args:
        start = int(request.args.get("start", "0"))

    return stream_with_context(
        stream_events(stream=stream, start=start, watch="X-Stream" in request.headers)
    )


def stream_events(
    stream: str, start: Optional[int] = None, watch: bool = False
) -> Iterator[str]:
    store = services.get_store().for_stream(stream)
    notifier = services.get_notifier()

    if watch and not notifier:
        raise HttpNotImplemented("Sorry, this server cannot stream events!")

    position_to_read = 0
    if start is not None:
        position_to_read = start
    elif last := store.last():
        position_to_read = (last.position or 0) + 1  # To please MyPy
    else:
        position_to_read = 0

    for e in store.read(position_to_read):
        yield event_to_string(e) + "\n"
        position_to_read = position_to_read + 1

    if watch:
        while True:
            time.sleep(0.01)
            if notifier.something_happened():
                for e in store.read(position_to_read):
                    yield event_to_string(e) + "\n"
                    position_to_read = position_to_read + 1

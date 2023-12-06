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

from flask import Flask

from bl_scrypture.infrastructure.flask import services, streams
from bl_scrypture.infrastructure.settings import WsgiSettings


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    app = Flask(__name__)
    app.register_blueprint(streams.blueprint, url_prefix="/")
    app.teardown_appcontext(services.close_session)
    return app

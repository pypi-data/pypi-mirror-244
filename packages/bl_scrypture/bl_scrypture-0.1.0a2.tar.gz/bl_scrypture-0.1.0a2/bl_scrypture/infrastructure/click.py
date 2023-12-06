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

from typing import Any

import click
from blessql.events import initialize

from bl_scrypture import __version__
from bl_scrypture.infrastructure.settings import CliSettings


@click.group()
def app() -> None:
    pass


@app.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    click.echo(__version__)
    ctx.exit(0)


@app.command()
@click.pass_context
def init_db(ctx: click.Context) -> None:
    """Initialise database's schema."""
    click.echo("Initialising schema…", nl=False)
    initialize(ctx.obj.DSN)
    click.echo(" OK!")
    ctx.exit(0)


def build_app(settings: CliSettings) -> Any:
    return app(obj=settings)

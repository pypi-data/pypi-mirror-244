# estory --- Read from and write to event stores
# Copyright © 2021-2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
from importlib import metadata
from pathlib import Path

import typer
from bles.utils import event_from_string, event_to_string

from .stores import build_store

__version__ = metadata.version(__package__ or __name__)

app = typer.Typer()


class CannotGuessIdentifier(Exception):
    pass


@app.command()
def guess(identifier: str) -> None:
    typer.echo(guess_real_identifier(identifier))


@app.command()
def init(identifier: str) -> None:
    real_identifier = guess_real_identifier(identifier)
    with build_store(real_identifier) as store:
        try:
            store.init()
            typer.echo(f"Database initialized. [identifier=`{real_identifier}`]")
        except Exception:
            typer.echo(f"Cannot initialize database! [identifier=`{real_identifier}`]")


@app.command()
def read(identifier: str) -> None:
    real_identifier = guess_real_identifier(identifier)
    with build_store(real_identifier) as store:
        for event in store.read():
            typer.echo(event_to_string(event))


@app.command()
def write(identifier: str, batch_size: int = 10) -> None:
    real_identifier = guess_real_identifier(identifier)
    with build_store(real_identifier) as store:
        events = []
        for line in sys.stdin:
            if data := line.strip():
                events.append(event_from_string(data))
                if len(events) >= batch_size:
                    store.record(events)
                    events.clear()
        if events:
            store.record(events)


def guess_real_identifier(identifier: str) -> str:
    if real_identifier := guess_real_identifier_from_env(identifier):
        return real_identifier
    if real_identifier := guess_real_identifier_from_uri(identifier):
        return real_identifier
    if real_identifier := guess_real_identifier_from_file(identifier):
        return real_identifier
    raise CannotGuessIdentifier(identifier)


def guess_real_identifier_from_env(identifier: str) -> str:
    if uri := os.environ.get(f"ESTORY_{identifier}"):
        return uri
    return ""


def guess_real_identifier_from_uri(identifier: str) -> str:
    if re.search(r"^[^:]+://.+$", identifier):
        return identifier
    return ""


def guess_real_identifier_from_file(identifier: str) -> str:
    if Path(identifier).exists():
        return f"sqlite:///{identifier}"
    return ""

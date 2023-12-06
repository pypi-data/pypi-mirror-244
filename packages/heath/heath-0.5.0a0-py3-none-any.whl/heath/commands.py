# heath --- Manage projections
# Copyright © 2022, 2023 Bioneland
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

from dataclasses import dataclass
from typing import Any, Callable

from bles import ProjectorStatuses
from blessql.projections import REGISTRY, Ledger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


@dataclass
class ProjectionInfo:
    name: str
    status: str
    position: int


class UnknownProjection(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown projection `{name}`!")


def session_maker(dsn: str) -> sessionmaker[Any]:
    return sessionmaker(bind=create_engine(dsn))


def initialise(dsn: str) -> None:
    REGISTRY.metadata.create_all(create_engine(dsn))


def status(dsn: str, echo: Callable[[str], None]) -> int:
    info = _collect_info(dsn)
    echo(_serialize_info(info))
    return _compute_exit_code(info)


def _collect_info(dsn: str) -> list[ProjectionInfo]:
    data: list[ProjectionInfo] = []
    with session_maker(dsn)() as session:
        ledger = Ledger(session)
        for name, status, position in ledger.status():
            data.append(ProjectionInfo(name, status.name, int(position)))
    return data


def _serialize_info(data: list[ProjectionInfo]) -> str:
    text = _status_summary(data)
    for d in data:
        text += f"\n[{d.status}] `{d.name}` at position {d.position}."
    return text


def _status_summary(data: list[ProjectionInfo]) -> str:
    if not data:
        return "UNKNOWN: no projections are registered."

    broken = [d for d in data if d.status == "BROKEN"]
    if broken:
        return (
            "CRITICAL: some projections are broken"
            + " ("
            + ", ".join([f"'{b.name}'" for b in broken])
            + ")."
        )
    other = [d for d in data if d.status != "BROKEN" and d.status != "OK"]
    if other:
        return (
            "WARNING: some projections are not OK"
            + " ("
            + ", ".join([f"'{o.name}'" for o in other])
            + ")."
        )
    return "OK: all projections are OK."


def _compute_exit_code(data: list[ProjectionInfo]) -> int:
    if not data:
        return 3
    if any([d.status == "BROKEN" for d in data]):
        return 2
    if any([d.status != "BROKEN" and d.status != "OK" for d in data]):
        return 1
    return 0


def purge(dsn: str, name: str) -> None:
    with session_maker(dsn)() as session:
        ledger = Ledger(session)
        if not ledger.knows(name):
            raise UnknownProjection(name)

        ledger.forget(name)
        session.commit()

    # Projection tables are not handled with the ORM.
    with create_engine(dsn).connect() as connection:
        connection.execute(text(f"DROP TABLE IF EXISTS {name}"))


def stall(dsn: str, name: str) -> None:
    with session_maker(dsn)() as session:
        ledger = Ledger(session)
        if not ledger.knows(name):
            raise UnknownProjection(name)

        ledger.mark_as(name, ProjectorStatuses.STALLED)
        session.commit()

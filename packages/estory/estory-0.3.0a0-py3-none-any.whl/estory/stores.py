# estory --- Read from and write to event stores
# Copyright © 2023 Bioneland
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

from abc import ABC, abstractmethod
from typing import Any, Iterator, Optional

import requests
from bles import Event
from bles.utils import event_from_string, event_to_string
from blessql.events import REGISTRY, EventStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Store(ABC):
    @abstractmethod
    def __enter__(self) -> "Store":
        ...

    @abstractmethod
    def __exit__(
        self,
        exception_type: Optional[str] = None,
        exception_value: Optional[Exception] = None,
        traceback: Optional[Any] = None,
    ) -> None:
        ...

    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def read(self, start: int = 0, follow: bool = False) -> Iterator[Event]:
        ...

    @abstractmethod
    def record(self, events: list[Event]) -> None:
        ...


class BlessqlStore(Store):
    def __init__(self, dsn: str) -> None:
        self.__dsn = dsn

    def __enter__(self) -> Store:
        session_maker = sessionmaker(bind=create_engine(self.__dsn))
        self.__session = session_maker()
        self.__session.begin()
        self.__store = EventStore(self.__session)
        return self

    def __exit__(
        self,
        exception_type: Optional[str] = None,
        exception_value: Optional[Exception] = None,
        traceback: Optional[Any] = None,
    ) -> None:
        if exception_type:
            self.__session.rollback()
        else:
            self.__session.commit()

    def init(self) -> None:
        REGISTRY.metadata.create_all(create_engine(self.__dsn))

    def read(self, start: int = 0, follow: bool = False) -> Iterator[Event]:
        return self.__store.read(start, follow)

    def record(self, events: list[Event]) -> None:
        self.__store.record(events)
        self.__session.commit()


class ScryptureStore(Store):
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__session = requests.session()

    def __enter__(self) -> Store:
        self.__session = requests.session()
        self.__store = HttpEventStore(self.__session, self.__url)
        return self

    def __exit__(
        self,
        exception_type: Optional[str] = None,
        exception_value: Optional[Exception] = None,
        traceback: Optional[Any] = None,
    ) -> None:
        self.__session.close()

    def init(self) -> None:
        raise RuntimeError("Scrypture stores cannot be initialized!")

    def read(self, start: int = 0, follow: bool = False) -> Iterator[Event]:
        return self.__store.read(start, follow)

    def record(self, events: list[Event]) -> None:
        self.__store.record(events)


class HttpEventStore(EventStore):
    def __init__(self, session: requests.Session, url: str) -> None:
        self.__session: requests.Session = session
        self.__url: str = url
        self.__stream: str = ""

    def record(self, events: list[Event]) -> None:
        url = self.__build_url()
        data = "\n".join([event_to_string(e) for e in events])
        with self.__session.post(url, headers=None, data=data) as r:
            if r.status_code != 201:
                raise Exception(f"[{r.status_code}] {r.text}")
        return None

    def __build_url(self, start: Optional[int] = None) -> str:
        url = self.__url
        if self.__stream:
            url = f"{url}/{self.__stream}"
        if start is not None:
            url = f"{url}?start={start}"
        return url

    def for_stream(self, name: str) -> "HttpEventStore":
        self.__stream = name
        return self

    def read(self, start: int = 0, follow: bool = False) -> Iterator[Event]:
        url = self.__build_url(start)
        with self.__session.get(url, headers={}, stream=False) as r:
            for line in r.iter_lines():
                if line:
                    yield event_from_string(line.decode())

    def last(self) -> Optional[Event]:
        raise NotImplementedError()


def build_store(identifier: str) -> Store:
    if identifier.startswith("http://") or identifier.startswith("https://"):
        return ScryptureStore(identifier)
    return BlessqlStore(identifier)

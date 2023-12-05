"""cdfs.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from abc import abstractmethod
import datetime
import pathlib
from typing import Any

# Third-Party Packages #
from baseobjects import BaseComposite
from baseobjects.cachingtools import CachingObject, timed_keyless_cache
from dspobjects.time import Timestamp
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Local Packages #
from ..contentsfile import TimeContentsFile
from ..arrays import TimeContentsProxy


# Definitions #
# Classes #
class CDFS(CachingObject, BaseComposite):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    default_component_types: dict[str, tuple[type, dict[str, Any]]] = {}
    default_proxy_type: type[TimeContentsProxy] = TimeContentsProxy
    default_data_file_type: type | None = None
    default_content_file_name: str = "contents.sqlite3"
    contents_file_type: type[TimeContentsFile] = TimeContentsFile

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: pathlib.Path | str | None = None,
        mode: str = "r",
        open_: bool = True,
        load: bool = True,
        create: bool = False,
        update: bool = False,
        contents_name: str | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._path: pathlib.Path | None = None
        self._is_open: bool = False
        self._mode: str = "r"
        self._swmr_mode: bool = False

        self.contents_file_name: str = self.default_content_file_name
        self.contents_file: TimeContentsFile | None = None

        self.data_file_type: type = self.default_data_file_type

        self._start_datetime: Timestamp | None = None
        self._end_datetime: Timestamp | None = None
        self.data: TimeContentsProxy | None = None

        self.components: dict[str, Any] = {}

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                mode=mode,
                open_=open_,
                load=load,
                create=create,
                update=update,
                contents_name=contents_name,
                **kwargs,
            )

    @property
    def path(self) -> pathlib.Path:
        """The path to the CDFS."""
        return self._path

    @path.setter
    def path(self, value: str | pathlib.Path) -> None:
        if isinstance(value, pathlib.Path) or value is None:
            self._path = value
        else:
            self._path = pathlib.Path(value)

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def contents_path(self) -> pathlib.Path:
        return self.path / self.contents_file_name

    @property
    def meta_information(self) -> dict[str, Any]:
        return self.contents_file.meta_information

    @property
    def start_datetime(self):
        if self._start_datetime is None or self.get_start_datetime.clear_condition():
            return self.get_start_datetime()
        return self._start_datetime

    @property
    def end_datimetime(self):
        if self._end_datetime is None or self.get_end_datetime.clear_condition():
            return self.get_end_datetime()
        return self._end_datetime

    def __bool__(self) -> bool:
        return self._is_open

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: pathlib.Path | str | None = None,
        mode: str | None = None,
        open_: bool = False,
        load: bool = False,
        create: bool = False,
        update: bool = False,
        contents_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path for this proxy to wrap.
            s_id: The subject ID.
            studies_path: The parent directory to this XLTEK study proxy.
            proxies: An iterable holding arrays/objects to store in this proxy.
            mode: Determines if the contents of this proxy are editable or not.
            update: Determines if this proxy will start_timestamp updating or not.
            open_: Determines if the arrays will remain open after construction.
            load: Determines if the arrays will be constructed.
            **kwargs: The keyword arguments to create contained arrays.
        """
        if path is not None:
            self.path = path

        if mode is not None:
            self._mode = mode
            
        if contents_name is not None:
            self.contents_file_name = contents_name

        super().construct(**kwargs)

        if open_ or load or create:
            self.open(load=load, create=create)

    # Contents File
    def open_contents_file(
        self,
        create: bool = False,
        **kwargs: Any,
    ) -> None:
        if not self.contents_path.is_file() and not create:
            raise ValueError("Contents file does not exist.")
        elif self.contents_file is None:
            self.contents_file = self.contents_file_type(
                path=self.contents_path,
                open_=True,
                create=create,
                **kwargs,
            )
        else:
            self.contents_file.open(**kwargs)
    
    # Meta Information
    def get_meta_information(self, session: Session | None = None) -> dict[str, Any]:
        return self.contents_file.get_meta_information(session=session)

    async def get_meta_information_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
    ) -> dict[str, Any]:
        return await self.contents_file.get_meta_information_async(session=session)

    def set_meta_information(
        self,
        session: Session | None = None,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        self.contents_file.create_meta_information(session=session, entry=entry, begin=begin, **kwargs)

    async def set_meta_information_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
        entry: dict[str, Any] | None = None,
        begin: bool = False,
        **kwargs: Any,
    ) -> None:
        await self.contents_file.create_meta_information_async(session=session, entry=entry, begin=begin, **kwargs)

    # Contents
    def correct_contents(self, session: Session | None = None, path: pathlib.Path | None = None) -> None:
        self.contents_file.correct_contents(session=session, path=self.path if path is None else path)

    async def correct_contents_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
        path: pathlib.Path | None = None,
    ) -> None:
        await self.contents_file.correct_contents_async(session=session, path=self.path if path is None else path)

    @timed_keyless_cache(call_method="clearing_call", local=True)
    def get_start_datetime(self, session: Session | None = None) -> Timestamp | None:
        self._start_datetime = self.contents_file.get_start_datetime(session=session)
        return self._start_datetime

    async def get_start_datetime_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
    ) -> Timestamp:
        self._start_datetime = await self.contents_file.get_start_datetime_async(session=session)
        self.get_start_datetime.refresh_expiration()
        return self._start_datetime

    @timed_keyless_cache(call_method="clearing_call", local=True)
    def get_end_datetime(self, session: Session | None = None) -> Timestamp:
        self._end_datetime = self.contents_file.get_end_datetime(session=session)
        return self._end_datetime

    async def get_end_datetime_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
    ) -> Timestamp:
        self._end_datetime = await self.contents_file.get_end_datetime_async(session=session)
        self.get_end_datetime.refresh_expiration()
        return self._end_datetime_datetime

    def get_contents_nanostamps(self, session: Session | None = None) -> tuple[tuple[int, int, int], ...]:
        return self.contents_file.get_contents_nanostamps(session=session)

    async def get_contents_nanostamps_async(
        self,
        session: async_sessionmaker[AsyncSession] | AsyncSession | None = None,
    ) -> tuple[tuple[int, int, int], ...]:
        return await self.contents_file.get_contents_nanostamps_async(session=session)

    # CDFS Data
    def construct_data(self, swmr: bool = True, **kwargs):
        self.data = self.default_proxy_type(
            path=self.path,
            contents_file=self.contents_file,
            mode=self._mode,
            swmr=swmr,
            **kwargs,
        )

    # File
    def create(self, **kwargs) -> None:
        self.path.mkdir(exist_ok=True)
        self.open_contents_file(create=True, **kwargs)

    def open(
        self,
        mode: str | None = None,
        load: bool | None = None,
        create: bool = False,
        **kwargs: Any,
    ) -> None:
        if not self._is_open:
            if mode is not None:
                self._mode = mode

            if not self.path.is_dir():
                if create:
                    self.create(**kwargs)
                else:
                    raise ValueError("Contents file does not exist.")
            else:
                self.open_contents_file(create=create, **kwargs)
                self.contents_file.get_meta_information()
            self._is_open = True

            if load:
                self.construct_data()

    def close(self):
        if self.contents_file is not None:
            self.contents_file.close()
        if self.data is not None:
            self.data.close()
        self._is_open = False
        return True

    async def close_async(self) -> bool:
        if self.contents_file is not None:
            await self.contents_file.close_async()
        if self.data is not None:
            self.data.close()
        self._is_open = False
        return True
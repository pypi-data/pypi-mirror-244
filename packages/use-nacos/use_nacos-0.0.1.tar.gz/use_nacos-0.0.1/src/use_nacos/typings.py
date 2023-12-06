from typing import Awaitable, Union, TypeVar

T = TypeVar("T")
SyncAsync = Union[T, Awaitable[T]]

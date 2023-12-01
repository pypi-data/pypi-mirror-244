import builtins
import sys
from typing import AsyncIterator, TypeVar

__all__ = ["anext"]

T = TypeVar("T")


if sys.version_info < (3, 10):

    async def anext(ait: AsyncIterator[T]) -> T:
        return await ait.__anext__()

else:
    anext = builtins.anext

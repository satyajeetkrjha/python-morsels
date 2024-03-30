from contextlib import contextmanager
from dataclasses import dataclass
from types import TracebackType
from typing import Iterator,Optional,Type


@dataclass
class ExceptionInfo:
    exception: Optional[Exception] =None
    traceback: Optional[TracebackType]=None


@contextmanager
def suppress(*exception_types):
    info = ExceptionInfo()
    try:
        yield info
    except exception_types as e:
        info.exception = e
        info.traceback = e.__traceback__        
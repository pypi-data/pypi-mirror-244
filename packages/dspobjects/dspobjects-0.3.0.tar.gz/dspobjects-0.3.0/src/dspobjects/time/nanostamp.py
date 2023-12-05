"""nanostamp.py
Create a nanostamp based on input
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
from datetime import datetime, timezone, date, tzinfo
import time

# Third-Party Packages #
from baseobjects.functions import singlekwargdispatch
from baseobjects.operations import timezone_offset
import numpy as np
import pandas as pd

# Local Packages #
from .timestamp import Timestamp, NANO_SCALE


# Definitions #
# Functions #
@singlekwargdispatch("value")
def nanostamp(
    value: datetime | date | float | int | np.dtype | np.ndarray,
    tz: tzinfo | None = None,
    is_nano: bool = False,
) -> np.uint64 | np.ndarray:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.
    """
    raise TypeError(f"the start cannot be assigned to a {type(value)}")


@nanostamp.register
def _nanostamp_uint64(value: np.uint64, tz: tzinfo | None = None, is_nano: bool = True) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    if not is_nano:
        value = value * NANO_SCALE
    return value if tz is None else value - (timezone_offset(tz).seconds * NANO_SCALE)


@nanostamp.register
def _nanostamp_pd_timestamp(value: pd.Timestamp, tz: tzinfo | None = None, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    if tz is not None:
        value = value.replace(tzinfo=tz)
    if value.tz is None:
        local_time = time.localtime()
        return np.uint64((value - Timestamp._UNIX_EPOCH - pd.Timedelta(seconds=local_time.tm_gmtoff)).value)
    else:
        return np.uint64((value.astimezone(timezone.utc) - Timestamp.UNIX_EPOCH).value)


@nanostamp.register
def _nanostamp_datetime(value: datetime, tz: tzinfo | None = None, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    if tz is not None:
        value = value.replace(tzinfo=tz)
    return np.uint64(value.timestamp() * NANO_SCALE)

@nanostamp.register
def _nanostamp_date(value: date, tz: tzinfo | None = None, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    return _nanostamp_pd_timestamp(Timestamp(value, tz=timezone.utc if tz is None else tz), is_nano=is_nano)

@nanostamp.register
def _nanostamp_array(value: np.ndarray, tz: tzinfo | None = None, is_nano: bool = False) -> np.ndarray:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        tz: The timezone of given value.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    if not is_nano:
        value = value * NANO_SCALE

    if tz is not None:
        value = value - (timezone_offset(tz).seconds * NANO_SCALE)

    return value.astype(np.uint64)


@nanostamp.register(float)
@nanostamp.register(int)
@nanostamp.register(np.dtype)
def _nanostamp(value: float | int | np.dtype, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.

    Returns:
        A nanostamp.
    """
    if is_nano:
        return np.uint64(value)
    else:
        return np.uint64(value * NANO_SCALE)

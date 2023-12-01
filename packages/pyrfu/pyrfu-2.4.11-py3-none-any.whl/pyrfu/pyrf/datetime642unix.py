#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def datetime642unix(time):
    r"""Converts datetime64 in ns units to unix time.

    Parameters
    ----------
    time : ndarray
        Time in datetime64 format.

    Returns
    -------
    time_unix : ndarray
        Time in unix format.

    See Also
    --------
    pyrfu.pyrf.unix2datetime64

    """

    # Make sure that time is in ns format
    if isinstance(time, np.datetime64):
        time = np.array([time])
        time_datetime64 = time.astype("datetime64[ns]")
    elif isinstance(time, (list, np.ndarray)) and isinstance(time[0], np.datetime64):
        time_datetime64 = time.astype("datetime64[ns]")
    else:
        raise TypeError("time must be numpy.datetime64 or array_like")

    # Convert to unix
    time_unix = time_datetime64.astype(np.int64) / 1e9

    return time_unix

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
import xarray as xr

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def ts_append(inp0, inp1):
    r"""Concatenate two time series along the time axis.

    Parameters
    ----------
    inp0 : xarray.DataArray
        Time series of the first input (early times).
    inp1 : xarray.DataArray
        Time series of the second input (late times).

    Returns
    -------
    out : xarray.DataArray
        Concatenated time series.

    Notes
    -----
    The time series must be in the correct time order.

    """

    if inp0 is None:
        return inp1

    out_data = {}

    if inp0.data.ndim != 1:
        out_data["data"] = np.vstack([inp0, inp1])

    else:
        out_data["data"] = np.hstack([inp0, inp1])

    out_data["attrs"] = {}

    for k in inp0.attrs:
        if isinstance(inp0.attrs[k], np.ndarray):
            out_data["attrs"][k] = np.hstack([inp0.attrs[k], inp1.attrs[k]])

        else:
            out_data["attrs"][k] = inp0.attrs[k]

    depends = [{} for _ in range(len(inp0.dims))]

    for i, dim in enumerate(inp0.dims):
        if i == 0 or dim == "time":
            depends[i]["data"] = np.hstack([inp0[dim].data, inp1[dim].data])

            # add attributes
            depends[i]["attrs"] = {}

            for k in inp0[dim].attrs:
                # if attrs is array time append
                if isinstance(inp0[dim].attrs[k], np.ndarray):
                    depends[i]["attrs"][k] = np.hstack(
                        [inp0[dim].attrs[k], inp1[dim].attrs[k]],
                    )

                else:
                    depends[i]["attrs"][k] = inp0[dim].attrs[k]

        else:
            # Use values of other coordinates of inp0 assuming equal to inp1
            depends[i]["data"] = inp0[dim].data

            # add attributes
            depends[i]["attrs"] = {}

            for k in inp0[dim].attrs:
                depends[i]["attrs"][k] = inp0[dim].attrs[k]

    # Create DataArray
    out = xr.DataArray(
        out_data["data"],
        coords=[depend["data"] for depend in depends],
        dims=inp0.dims,
        attrs=out_data["attrs"],
    )

    for i, dim in enumerate(out.dims):
        out[dim].attrs = depends[i]["attrs"]

    return out

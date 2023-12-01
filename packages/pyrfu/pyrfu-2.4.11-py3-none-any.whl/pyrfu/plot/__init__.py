#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import matplotlib.pyplot as plt

from .add_position import add_position
from .annotate_heatmap import annotate_heatmap
from .colorbar import colorbar
from .make_labels import make_labels
from .mms_pl_config import mms_pl_config
from .pl_scatter_matrix import pl_scatter_matrix
from .pl_tx import pl_tx
from .plot_ang_ang import plot_ang_ang
from .plot_clines import plot_clines
from .plot_heatmap import plot_heatmap

# Local imports
from .plot_line import plot_line
from .plot_magnetosphere import plot_magnetosphere
from .plot_projection import plot_projection
from .plot_reduced_2d import plot_reduced_2d
from .plot_sitl_overview import plot_sitl_overview
from .plot_spectr import plot_spectr
from .plot_surf import plot_surf
from .span_tint import span_tint
from .zoom import zoom

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


# Setup plotting style
plt.style.use("classic")
plt.rcParams["figure.facecolor"] = "1"
plt.rcParams["mathtext.sf"] = "sans"
plt.rcParams["mathtext.fontset"] = "dejavusans"

__all__ = [
    "add_position",
    "annotate_heatmap",
    "colorbar",
    "make_labels",
    "mms_pl_config",
    "pl_scatter_matrix",
    "pl_tx",
    "plot_ang_ang",
    "plot_clines",
    "plot_heatmap",
    "plot_line",
    "plot_magnetosphere",
    "plot_projection",
    "plot_reduced_2d",
    "plot_sitl_overview",
    "plot_spectr",
    "plot_surf",
    "span_tint",
    "zoom",
]

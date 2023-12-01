import numpy as np
from ._contour_base import ContourBase


class ContourLineFig(ContourBase):
    def __init__(self, fig=None):
        super().__init__(fig)

    def set_grid_data(self, X, Y, Z, value):
        self._axes.contour(X, Y, Z, levels=[value], colors="#7CFC00", linewidths=1.5)

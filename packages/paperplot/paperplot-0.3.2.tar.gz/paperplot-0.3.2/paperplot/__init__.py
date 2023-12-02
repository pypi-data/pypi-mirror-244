import matplotlib as mpl
from .contour_fig import ContourFig
from .contour_grid_filter import ContourGridFilter
from .contour_line_fig import ContourLineFig
from .contour_points_filter import ContourPointsFilter
from .line_fig import LineFig
from .line_style import LineStyle
from .mesh_fig import MeshFig
from .pixel_contour_fig import PixelContourFig
from .pixel_grid_filter import PixelGridFilter

# set global font
mpl.rcParams["font.family"] = ["Times New Roman"]
# set global font size
mpl.rcParams["font.size"] = 20
# set global math font
mpl.rcParams["mathtext.fontset"] = "stix"
# set round numbers
mpl.rcParams["axes.autolimit_mode"] = "round_numbers"

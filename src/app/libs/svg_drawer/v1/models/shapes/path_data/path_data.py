from typing import Union

from app.libs.svg_drawer.v1.models.shapes.path_data.arc import Arc
from app.libs.svg_drawer.v1.models.shapes.path_data.close_path import ClosePath
from app.libs.svg_drawer.v1.models.shapes.path_data.cubic_bezier import CubicBezier
from app.libs.svg_drawer.v1.models.shapes.path_data.horizontal_line import HorizontalLine
from app.libs.svg_drawer.v1.models.shapes.path_data.line_to import LineTo
from app.libs.svg_drawer.v1.models.shapes.path_data.move_to import MoveTo
from app.libs.svg_drawer.v1.models.shapes.path_data.quadratic_bezier import QuadraticBezier
from app.libs.svg_drawer.v1.models.shapes.path_data.smooth_cubic_bezier import SmoothCubicBezier
from app.libs.svg_drawer.v1.models.shapes.path_data.smooth_quadratic_bezier import (
    SmoothQuadraticBezier,
)
from app.libs.svg_drawer.v1.models.shapes.path_data.vertical_line import VerticalLine

PathData = Union[
    MoveTo,
    LineTo,
    HorizontalLine,
    VerticalLine,
    CubicBezier,
    SmoothCubicBezier,
    QuadraticBezier,
    SmoothQuadraticBezier,
    Arc,
    ClosePath,
]

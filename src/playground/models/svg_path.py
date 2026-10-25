from typing import Literal, Union, List, Optional
from pydantic import BaseModel, Field

class MoveTo(BaseModel):
    """Moves the pen to the specified coordinates without drawing."""
    command: Literal["M", "m"] = Field(..., description="Command character: M (absolute) or m (relative).")
    x: float = Field(..., description="X coordinate of the destination point.")
    y: float = Field(..., description="Y coordinate of the destination point.")

class LineTo(BaseModel):
    """Draws a straight line from the current position to the destination."""
    command: Literal["L", "l"] = Field(..., description="Command character: L (absolute) or l (relative).")
    x: float = Field(..., description="X coordinate of the line endpoint.")
    y: float = Field(..., description="Y coordinate of the line endpoint.")

class HorizontalLineTo(BaseModel):
    """Draws a horizontal straight line from the current position."""
    command: Literal["H", "h"] = Field(..., description="Command character: H (absolute) or h (relative).")
    x: float = Field(..., description="X coordinate of the horizontal endpoint.")

class VerticalLineTo(BaseModel):
    """Draws a vertical straight line from the current position."""
    command: Literal["V", "v"] = Field(..., description="Command character: V (absolute) or v (relative).")
    y: float = Field(..., description="Y coordinate of the vertical endpoint.")

class CubicBezier(BaseModel):
    """Draws a cubic Bézier curve using two control points."""
    command: Literal["C", "c"] = Field(..., description="Command character: C (absolute) or c (relative).")
    x1: float = Field(..., description="X coordinate of the first control point.")
    y1: float = Field(..., description="Y coordinate of the first control point.")
    x2: float = Field(..., description="X coordinate of the second control point.")
    y2: float = Field(..., description="Y coordinate of the second control point.")
    x: float = Field(..., description="X coordinate of the curve endpoint.")
    y: float = Field(..., description="Y coordinate of the curve endpoint.")

class SmoothCubic(BaseModel):
    """Draws a smooth continuation cubic Bézier curve."""
    command: Literal["S", "s"] = Field(..., description="Command character: S (absolute) or s (relative).")
    x2: float = Field(..., description="X coordinate of the second control point.")
    y2: float = Field(..., description="Y coordinate of the second control point.")
    x: float = Field(..., description="X coordinate of the curve endpoint.")
    y: float = Field(..., description="Y coordinate of the curve endpoint.")

class QuadraticBezier(BaseModel):
    """Draws a quadratic Bézier curve using a single control point."""
    command: Literal["Q", "q"] = Field(..., description="Command character: Q (absolute) or q (relative).")
    x1: float = Field(..., description="X coordinate of the control point.")
    y1: float = Field(..., description="Y coordinate of the control point.")
    x: float = Field(..., description="X coordinate of the curve endpoint.")
    y: float = Field(..., description="Y coordinate of the curve endpoint.")

class SmoothQuadratic(BaseModel):
    """Draws a smooth continuation quadratic Bézier curve."""
    command: Literal["T", "t"] = Field(..., description="Command character: T (absolute) or t (relative).")
    x: float = Field(..., description="X coordinate of the curve endpoint.")
    y: float = Field(..., description="Y coordinate of the curve endpoint.")

class EllipticalArc(BaseModel):
    """Draws an elliptical arc segment."""
    command: Literal["A", "a"] = Field(..., description="Command character: A (absolute) or a (relative).")
    rx: float = Field(..., description="Radius along the x-axis.")
    ry: float = Field(..., description="Radius along the y-axis.")
    x_axis_rotation: float = Field(..., description="Rotation angle of the ellipse x-axis in degrees.")
    large_arc_flag: int = Field(..., ge=0, le=1, description="Large arc flag (0 for arc <= 180°, 1 for arc > 180°).")
    sweep_flag: int = Field(..., ge=0, le=1, description="Sweep flag (0 for counter-clockwise, 1 for clockwise).")
    x: float = Field(..., description="X coordinate of the arc endpoint.")
    y: float = Field(..., description="Y coordinate of the arc endpoint.")

class ClosePath(BaseModel):
    """Closes the current subpath by drawing a straight line to the start point."""
    command: Literal["Z", "z"] = Field(..., description="Command character: Z or z to close the path.")

PathCommand = Union[
    MoveTo,
    LineTo,
    HorizontalLineTo,
    VerticalLineTo,
    CubicBezier,
    SmoothCubic,
    QuadraticBezier,
    SmoothQuadratic,
    EllipticalArc,
    ClosePath
]

class SVGPath(BaseModel):
    """Complete data model representing an SVG <path> element including XML attributes."""
    id: Optional[str] = Field(None, description="The unique identifier of the path element.")
    stroke: Optional[str] = Field(None, description="Color of the path stroke.")
    stroke_width: Optional[float] = Field(None, alias="stroke-width", description="Width of the path stroke.")
    fill: Optional[str] = Field(None, description="Fill color of the path shape.")
    commands: List[PathCommand] = Field(..., description="Ordered list of drawing commands inside the 'd' attribute.")

    class Config:
        populate_by_name = True
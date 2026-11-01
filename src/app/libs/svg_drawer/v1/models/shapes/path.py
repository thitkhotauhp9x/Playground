import re
from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import Field, field_validator

from app.libs.svg_drawer.v1.models.shapes.shape import Shape


class PathShape(Shape):
    """An SVG path supporting standard move, line, curve, arc, and close commands."""

    shape_type: Literal["path"] = "path"
    d: str = Field(
        description=(
            "SVG path data using M, L, H, V, C, S, Q, T, A, and Z commands; "
            "use C or Q for smooth curves"
        ),
        min_length=1,
        max_length=4000,
    )
    fill: str = Field(default="none", description="Fill color or none")
    stroke: str = Field(default="#3D342F", description="Stroke color")
    stroke_width: float = Field(default=2.5, gt=0, le=20, description="Stroke width")

    @field_validator("d")
    @classmethod
    def validate_path_commands(cls, value: str) -> str:
        if not re.fullmatch(r"[MmLlHhVvCcSsQqTtAaZz0-9eE.,+\-\s]+", value):
            raise ValueError("Path data contains unsupported SVG commands or characters")
        if not re.search(r"[Mm]", value):
            raise ValueError("SVG path data must begin with a move command")
        return value.strip()

    def to_svg(self) -> Element:
        return Element(
            "path",
            attrib={
                "id": self.shape_id,
                "d": self.d,
                "fill": self.fill,
                "stroke": self.stroke,
                "stroke-width": str(self.stroke_width),
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
        )

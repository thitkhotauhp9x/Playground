from typing import Annotated, Literal
from xml.etree.ElementTree import Element

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.path_data import PathData
from app.libs.svg_drawer.v1.models.shapes.shape import Shape


class PathShape(Shape):
    """An SVG path supporting standard move, line, curve, arc, and close commands."""

    shape_type: Literal["path"] = "path"
    d: list[Annotated[PathData, Field(discriminator="command")]] = Field(
        default_factory=list, description="SVG path data"
    )
    fill: str = Field(default="none", description="Fill color or none")
    stroke: str = Field(default="#3D342F", description="Stroke color")
    stroke_width: float = Field(default=2.5, gt=0, le=20, description="Stroke width")

    def to_svg(self) -> Element:
        return Element(
            "path_data",
            attrib={
                "id": self.shape_id,
                "d": " ".join([i.to_svg_string() for i in self.d]),
                "fill": self.fill,
                "stroke": self.stroke,
                "stroke-width": str(self.stroke_width),
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            },
        )

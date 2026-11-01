from typing import Literal
from xml.etree.ElementTree import Element

from app.libs.svg_drawer.v1.models.shapes.shape import Shape


class Rect(Shape):
    shape_type: Literal["rect"] = "rect"
    width: int
    height: int
    x: int
    y: int
    rx: int
    ry: int
    fill: str
    stroke: str = "#3D342F"
    stroke_width: float = 2.5

    def to_svg(self) -> Element:
        attrs = {
            "id": str(self.shape_id),
            "width": str(self.width),
            "height": str(self.height),
            "x": str(self.x),
            "y": str(self.y),
            "rx": str(self.rx),
            "ry": str(self.ry),
            "fill": self.fill,
            "stroke": self.stroke,
            "stroke-width": str(self.stroke_width),
        }
        return Element("rect", attrib=attrs)

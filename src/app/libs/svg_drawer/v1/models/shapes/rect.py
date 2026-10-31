from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import BaseModel


class Rect(BaseModel):
    shape_type: Literal["rect"] = "rect"
    id: str
    width: int
    height: int
    x: int
    y: int
    rx: int
    ry: int
    fill: str

    def to_svg(self) -> Element:
        attrs = {
            "id": str(self.id),
            "width": str(self.width),
            "height": str(self.height),
            "x": str(self.x),
            "y": str(self.y),
            "rx": str(self.rx),
            "ry": str(self.ry),
            "fill": self.fill,
        }
        return Element("rect", attrib=attrs)

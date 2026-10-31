from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field


class Line(BaseModel):
    shape_type: Literal["line"] = "line"
    id: str
    x1: float | int = Field(default=0, description="Tọa độ x điểm bắt đầu")
    y1: float | int = Field(default=0, description="Tọa độ y điểm bắt đầu")
    x2: float | int = Field(description="Tọa độ x điểm kết thúc")
    y2: float | int = Field(description="Tọa độ y điểm kết thúc")

    def to_svg(self) -> Element:
        svg_element = Element("line", attrib={
            "id": self.id,
            "x1": str(self.x1),
            "y1": str(self.y1),
            "x2": str(self.x2),
            "y2": str(self.y2),
            "stroke": "black",
        })
        return svg_element

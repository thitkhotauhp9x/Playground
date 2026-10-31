from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.shape import Shape


class Ellipse(Shape):
    shape_type: Literal["ellipse"] = "ellipse"
    rx: float | int = Field(description="Bán kính hình elip theo trục x")
    ry: float | int = Field(description="Bán kính hình elip theo trục y")
    cx: float | int = Field(default=0, description="Tọa độ tâm x")
    cy: float | int = Field(default=0, description="Tọa độ tâm y")
    fill: str = Field(description="Màu sắc tô nền")

    def to_svg(self) -> Element:
        svg_element = Element(
            "ellipse",
            attrib={
                "id": self.shape_id,
                "rx": str(self.rx),
                "ry": str(self.ry),
                "cx": str(self.cx),
                "cy": str(self.cy),
                "fill": self.fill,
            },
        )
        return svg_element

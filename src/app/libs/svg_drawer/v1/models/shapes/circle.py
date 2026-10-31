from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.shape import Shape


class Circle(Shape):
    shape_type: Literal["circle"] = "circle"
    r: float | int = Field(description="Bán kính hình tròn")
    cx: float | int = Field(default=0, description="Tọa độ tâm x")
    cy: float | int = Field(default=0, description="Tọa độ tâm y")
    fill: str = Field(description="Màu sắc tô nền")

    def to_svg(self) -> Element:
        svg_element = Element(
            "circle",
            attrib={
                "id": self.shape_id,
                "r": str(self.r),
                "cx": str(self.cx),
                "cy": str(self.cy),
                "fill": self.fill,
            },
        )
        return svg_element

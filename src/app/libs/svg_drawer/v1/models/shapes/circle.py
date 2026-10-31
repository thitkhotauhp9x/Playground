from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field


class Circle(BaseModel):
    shape_type: Literal["circle"] = "circle"
    id: str = Field(alias="id", description="Mã định danh ID")
    r: float | int = Field(description="Bán kính hình tròn")
    cx: float | int = Field(default=0, description="Tọa độ tâm x")
    cy: float | int = Field(default=0, description="Tọa độ tâm y")
    fill: str = Field(description="Màu sắc tô nền")

    def to_svg(self) -> Element:
        svg_element = Element(
            "circle",
            attrib={
                "id": self.id,
                "r": str(self.r),
                "cx": str(self.cx),
                "cy": str(self.cy),
                "fill": self.fill,
            },
        )
        return svg_element

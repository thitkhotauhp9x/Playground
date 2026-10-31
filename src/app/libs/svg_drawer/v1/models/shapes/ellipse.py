from typing import Literal
from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field


class Ellipse(BaseModel):
    shape_type: Literal["ellipse"] = "ellipse"
    rx: float | int = Field(description="Bán kính hình elip theo trục x")
    ry: float | int = Field(description="Bán kính hình elip theo trục y")
    cx: float | int = Field(default=0, description="Tọa độ tâm x")
    cy: float | int = Field(default=0, description="Tọa độ tâm y")
    fill: str = Field(description="Màu sắc tô nền")
    id: str = Field(alias="id", description="Mã định danh ID")

    def to_svg(self) -> Element:
        svg_element = Element(
            "ellipse",
            attrib={
                "id": self.id,
                "rx": str(self.rx),
                "ry": str(self.ry),
                "cx": str(self.cx),
                "cy": str(self.cy),
                "fill": self.fill,
            },
        )
        return svg_element

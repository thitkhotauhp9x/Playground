from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class SmoothCubicBezier(BasePathData):
    command: Literal["S", "s"] = Field(..., description="Lệnh S hoặc s")
    x2: float
    y2: float
    x: float
    y: float

    def to_svg_string(self) -> str:
        return f"{self.command} {self.x2} {self.y2} {self.x} {self.y}"

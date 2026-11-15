from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class QuadraticBezier(BasePathData):
    command: Literal["Q", "q"] = Field(..., description="Lệnh Q hoặc q")
    x1: float
    y1: float
    x: float
    y: float

    def to_svg_string(self) -> str:
        return f"{self.command} {self.x1} {self.y1} {self.x} {self.y}"

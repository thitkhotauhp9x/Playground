from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class VerticalLine(BasePathData):
    command: Literal["v", "V"] = Field(..., description="Lệnh V hoặc v")
    y: float

    def to_svg_string(self) -> str:
        return f"{self.command} {self.y}"

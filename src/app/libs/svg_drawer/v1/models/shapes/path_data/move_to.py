from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class MoveTo(BasePathData):
    command: Literal["M", "m"] = Field(..., description="Lệnh M hoặc m")
    x: float
    y: float

    def to_svg_string(self) -> str:
        return f"{self.command} {self.x} {self.y}"

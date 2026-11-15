from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class HorizontalLine(BasePathData):
    command: Literal["H", "h"] = Field(..., description="Lệnh H hoặc h")
    x: float

    def to_svg_string(self) -> str:
        return f"{self.command} {self.x}"

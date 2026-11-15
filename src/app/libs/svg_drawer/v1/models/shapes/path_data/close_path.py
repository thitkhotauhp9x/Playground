from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class ClosePath(BasePathData):
    command: Literal["Z", "z"] = Field(..., description="Lệnh Z hoặc z")

    def to_svg_string(self) -> str:
        return self.command

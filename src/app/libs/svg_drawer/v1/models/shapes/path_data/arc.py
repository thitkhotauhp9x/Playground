from typing import Literal

from pydantic import Field

from app.libs.svg_drawer.v1.models.shapes.path_data.base_path_data import BasePathData


class Arc(BasePathData):
    command: Literal["A", "a"] = Field(..., description="Lệnh A hoặc a")
    rx: float
    ry: float
    x_axis_rotation: float = Field(..., alias="x-axis-rotation")
    large_arc_flag: int = Field(..., ge=0, le=1, alias="large-arc-flag")
    sweep_flag: int = Field(..., ge=0, le=1, alias="sweep-flag")
    x: float
    y: float

    class Config:
        populate_by_name = True

    def to_svg_string(self) -> str:
        return (
            f"{self.command} {self.rx} {self.ry} {self.x_axis_rotation}"
            f" {self.large_arc_flag} {self.sweep_flag} {self.x} {self.y}"
        )

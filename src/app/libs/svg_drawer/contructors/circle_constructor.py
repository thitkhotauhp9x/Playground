from pydantic import BaseModel
from langchain.tools import tool
from app.libs.svg_drawer.models.shapes.circle import Circle
from app.libs.svg_drawer.models.svg import Svg


class Drawer(BaseModel):
    svg: Svg

    def draw_circle(self, circle_id: str, r: float | int, cx: float | int, cy: float, fill: str) -> None:
        """
        Vẽ một hình tròn

        Args:
            circle_id: Mã định danh hình tròn
            r: Bán kính hình tròn
            cx: Toạ độ tâm x
            cy: Toạ độ tâm y
            fill: Màu sắc tô nền

        Returns: None
        """
        circle = Circle(
            id=circle_id,
            r=r,
            cx=cx,
            cy=cy,
            fill=fill,
        )
        self.svg.shapes.append(circle)


drawer = Drawer(svg=Svg(shapes=[]))
drawer.draw_circle()
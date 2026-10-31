from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.shapes.eclipse import Eclipse
from app.libs.svg_drawer.v1.models.shapes.line import Line
from app.libs.svg_drawer.v1.models.shapes.rect import Rect


class SvgDrawer:
    def __init__(self, state: GraphState):
        self._state = state

    def draw_line(
        self, line_id: str, x1: float | int, x2: float | int, y1: float | int, y2: float | int
    ):
        """
        Draw a line
        Args:
            line_id: Mã định danh của đoạn thẳng
            x1: Toạ độ x điểm bắt đầu
            x2: Toạ độ x điểm kết thúc
            y1: Toạ độ y điểm bắt đầu
            y2: Toạ độ y điểm kết thúc

        Returns: None

        """
        line = Line(id=line_id, x1=x1, x2=x2, y1=y1, y2=y2)
        self._state.svg.shapes.append(line)

    def draw_circle(self, circle_id: str, r, cx, cy, fill):
        """
        Draw a circle
        Args:
            circle_id: mã định danh của đường tròn
            r: Bán kính hình tròn
            cx: Toạ độ tâm x
            cy: Toạ độ tâm y
            fill: Màu sắc tô nền

        Returns: None
        """
        circle = Circle(id=circle_id, r=r, cx=cx, cy=cy, fill=fill)
        self._state.svg.shapes.append(circle)

    def draw_eclipse(self, eclipse_id, rx, ry, cx, cy, fill):
        """
        Draw a eclipse
        Args:
            eclipse_id: Mã định danh của hình eclipse
            rx: Bán kính hình elip theo trục x
            ry: Bán kính hình elip theo trục y
            cx: Toạ độ tâm x
            cy: Toạ độ tâm y
            fill: Màu sắc tô nền

        Returns: None
        """
        eclipse = Eclipse(id=eclipse_id, rx=rx, ry=ry, cx=cx, cy=cy, fill=fill)
        self._state.svg.shapes.append(eclipse)

    def draw_rect(self, rect_id, width, height, x, y, rx, ry, fill):
        """
        Draw a rect
        Args:
            rect_id: Mã định danh của hình chữ nhật
            width: Required. The width of the rectangle
            height: Required. The height of the rectangle
            x: The x-position for the top-left corner of the rectangle
            y: The y-position for the top-left corner of the rectangle
            rx: The x radius of the corners of the rectangle
             (used to round the corners). Default is 0
            ry: The y radius of the corners of the rectangle
             (used to round the corners). Default is 0
            fill: Màu sắc tô nền

        Returns: None

        """
        rect = Rect(id=rect_id, width=width, height=height, x=x, y=y, rx=rx, ry=ry, fill=fill)
        self._state.svg.shapes.append(rect)

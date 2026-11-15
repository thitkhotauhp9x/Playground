from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.shapes.ellipse import Ellipse
from app.libs.svg_drawer.v1.models.shapes.line import Line
from app.libs.svg_drawer.v1.models.shapes.path import PathShape
from app.libs.svg_drawer.v1.models.shapes.path_data.path_data import PathData
from app.libs.svg_drawer.v1.models.shapes.rect import Rect
from app.libs.svg_drawer.v1.models.shapes.shape import Shape
from app.libs.svg_drawer.v1.models.svg import Svg


class SvgDrawer:
    def __init__(self, svg: Svg):
        self._svg = svg

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
        line = Line(shape_id=line_id, x1=x1, x2=x2, y1=y1, y2=y2)
        self._svg.shapes.append(line)

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
        circle = Circle(shape_id=circle_id, r=r, cx=cx, cy=cy, fill=fill)
        self._svg.shapes.append(circle)

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
        eclipse = Ellipse(shape_id=eclipse_id, rx=rx, ry=ry, cx=cx, cy=cy, fill=fill)
        self._svg.shapes.append(eclipse)

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
        rect = Rect(shape_id=rect_id, width=width, height=height, x=x, y=y, rx=rx, ry=ry, fill=fill)
        self._svg.shapes.append(rect)

    def draw_path(
        self,
        path_id: str,
        d: list[PathData],
        fill: str = "none",
        stroke: str = "#3D342F",
        stroke_width: float = 2.5,
    ) -> None:
        """
        Draw a freeform SVG path, including smooth curves and closed silhouettes.

        Args:
            path_id:
            d:{
                "$defs": {
                    "Arc": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh A ho\u1eb7c a",
                                "enum": [
                                    "A",
                                    "a"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "rx": {
                                "title": "Rx",
                                "type": "number"
                            },
                            "ry": {
                                "title": "Ry",
                                "type": "number"
                            },
                            "x-axis-rotation": {
                                "title": "X-Axis-Rotation",
                                "type": "number"
                            },
                            "large-arc-flag": {
                                "maximum": 1,
                                "minimum": 0,
                                "title": "Large-Arc-Flag",
                                "type": "integer"
                            },
                            "sweep-flag": {
                                "maximum": 1,
                                "minimum": 0,
                                "title": "Sweep-Flag",
                                "type": "integer"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "rx",
                            "ry",
                            "x-axis-rotation",
                            "large-arc-flag",
                            "sweep-flag",
                            "x",
                            "y"
                        ],
                        "title": "Arc",
                        "type": "object"
                    },
                    "ClosePath": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh Z ho\u1eb7c z",
                                "enum": [
                                    "Z",
                                    "z"
                                ],
                                "title": "Command",
                                "type": "string"
                            }
                        },
                        "required": [
                            "command"
                        ],
                        "title": "ClosePath",
                        "type": "object"
                    },
                    "CubicBezier": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh C ho\u1eb7c c",
                                "enum": [
                                    "C",
                                    "c"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x1": {
                                "title": "X1",
                                "type": "number"
                            },
                            "y1": {
                                "title": "Y1",
                                "type": "number"
                            },
                            "x2": {
                                "title": "X2",
                                "type": "number"
                            },
                            "y2": {
                                "title": "Y2",
                                "type": "number"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x1",
                            "y1",
                            "x2",
                            "y2",
                            "x",
                            "y"
                        ],
                        "title": "CubicBezier",
                        "type": "object"
                    },
                    "HorizontalLine": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh H ho\u1eb7c h",
                                "enum": [
                                    "H",
                                    "h"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x"
                        ],
                        "title": "HorizontalLine",
                        "type": "object"
                    },
                    "LineTo": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh L ho\u1eb7c l",
                                "enum": [
                                    "L",
                                    "l"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x",
                            "y"
                        ],
                        "title": "LineTo",
                        "type": "object"
                    },
                    "MoveTo": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh M ho\u1eb7c m",
                                "enum": [
                                    "M",
                                    "m"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x",
                            "y"
                        ],
                        "title": "MoveTo",
                        "type": "object"
                    },
                    "QuadraticBezier": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh Q ho\u1eb7c q",
                                "enum": [
                                    "Q",
                                    "q"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x1": {
                                "title": "X1",
                                "type": "number"
                            },
                            "y1": {
                                "title": "Y1",
                                "type": "number"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x1",
                            "y1",
                            "x",
                            "y"
                        ],
                        "title": "QuadraticBezier",
                        "type": "object"
                    },
                    "SmoothCubicBezier": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh S ho\u1eb7c s",
                                "enum": [
                                    "S",
                                    "s"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x2": {
                                "title": "X2",
                                "type": "number"
                            },
                            "y2": {
                                "title": "Y2",
                                "type": "number"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x2",
                            "y2",
                            "x",
                            "y"
                        ],
                        "title": "SmoothCubicBezier",
                        "type": "object"
                    },
                    "SmoothQuadraticBezier": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh T ho\u1eb7c t",
                                "enum": [
                                    "T",
                                    "t"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "x",
                            "y"
                        ],
                        "title": "SmoothQuadraticBezier",
                        "type": "object"
                    },
                    "VerticalLine": {
                        "properties": {
                            "command": {
                                "description": "L\u1ec7nh V ho\u1eb7c v",
                                "enum": [
                                    "v",
                                    "V"
                                ],
                                "title": "Command",
                                "type": "string"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            }
                        },
                        "required": [
                            "command",
                            "y"
                        ],
                        "title": "VerticalLine",
                        "type": "object"
                    }
                },
                "items": {
                    "anyOf": [
                        {
                            "$ref": "#/$defs/MoveTo"
                        },
                        {
                            "$ref": "#/$defs/LineTo"
                        },
                        {
                            "$ref": "#/$defs/HorizontalLine"
                        },
                        {
                            "$ref": "#/$defs/VerticalLine"
                        },
                        {
                            "$ref": "#/$defs/CubicBezier"
                        },
                        {
                            "$ref": "#/$defs/SmoothCubicBezier"
                        },
                        {
                            "$ref": "#/$defs/QuadraticBezier"
                        },
                        {
                            "$ref": "#/$defs/SmoothQuadraticBezier"
                        },
                        {
                            "$ref": "#/$defs/Arc"
                        },
                        {
                            "$ref": "#/$defs/ClosePath"
                        }
                    ]
                },
                "title": "DataPathList",
                "type": "array"
            }
            fill:
            stroke:
            stroke_width:

        Returns:

        """
        import pdb

        pdb.set_trace()
        self._svg.shapes.append(
            PathShape(
                shape_id=path_id,
                d=d,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
            )
        )

    def delete_shape(self, shape_id: str) -> None:
        """
        Delete a shape by its id
        Args:
            shape_id: Shape id

        Returns: None

        """
        for shape in self._svg.shapes:
            if isinstance(shape, Shape):
                if shape_id == shape.shape_id:
                    self._svg.shapes.remove(shape)
                    self._svg.display()
            else:
                raise TypeError("type(shape) != Shape")

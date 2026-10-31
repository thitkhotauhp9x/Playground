import abc
import tempfile
import webbrowser
from pathlib import Path
from typing import Annotated, Protocol, runtime_checkable
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field

from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.shapes.ellipse import Ellipse
from app.libs.svg_drawer.v1.models.shapes.line import Line
from app.libs.svg_drawer.v1.models.shapes.rect import Rect


@runtime_checkable
class SvgConverter(Protocol):
    @abc.abstractmethod
    def to_svg(self) -> Element:
        pass


class Svg(BaseModel):
    shapes: list[Annotated[Circle | Rect | Ellipse | Line, Field(discriminator="shape_type")]] = []
    height: int = 200
    width: int = 300

    def to_svg(self) -> Element:
        svg_element = Element(
            "svg",
            attrib={
                "height": str(self.height),
                "width": str(self.width),
                "xmlns": "http://www.w3.org/2000/svg",
            },
        )

        for shape in self.shapes:
            if isinstance(shape, SvgConverter):
                svg_element.append(shape.to_svg())
            else:
                raise TypeError("Unsupported shape type")
        return svg_element

    def display(self):
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp_file:
            file_path = Path(temp_file.name)
            svg_code = ElementTree.tostring(self.to_svg(), encoding="utf-8")
            file_path.write_bytes(svg_code)
            webbrowser.open(f"file://{file_path.as_posix()}")

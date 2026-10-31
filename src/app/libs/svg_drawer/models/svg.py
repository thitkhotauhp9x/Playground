import tempfile
from pathlib import Path
from typing import Protocol, runtime_checkable, Annotated
from xml.dom.minidom import Element
import webbrowser
from pydantic import BaseModel, Field
from xml.etree import ElementTree

from app.libs.svg_drawer.models.shapes.circle import Circle
from app.libs.svg_drawer.models.shapes.rect import Rect
from app.libs.svg_drawer.models.shapes.eclipse import Eclipse
from app.libs.svg_drawer.models.shapes.line import Line


@runtime_checkable
class SvgConverter(Protocol):
    def to_svg(self) -> Element:
        pass

class Svg(BaseModel):
    shapes: list[Annotated[Circle | Rect | Eclipse | Line, Field(discriminator="shape_type")]] = []
    height: int = 200
    width: int = 300

    def to_svg(self) -> Element:
        svg_element = ElementTree.Element("svg", attrib={
            "height": str(self.height),
            "width": str(self.width),
            "xmlns": "http://www.w3.org/2000/svg",
        })

        for shape in self.shapes:
            if isinstance(shape, SvgConverter):
                svg_element.append(shape.to_svg())
        return svg_element

    def display(self):
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp_file:
            file_path = Path(temp_file.name)
            svg_code = ElementTree.tostring(self.to_svg(), encoding="unicode")
            file_path.write_text(svg_code, encoding="utf-8")
            webbrowser.open(f"file://{file_path.as_posix()}")

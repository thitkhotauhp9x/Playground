from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated
from xml.etree import ElementTree

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

from app.libs.svg_drawer.models.svg import Svg
from app.libs.svg_drawer.svg_drawer import SvgDrawer

svg_drawer = APIRouter(tags=["svg-drawer"])


class SvgDrawerInput(BaseModel):
    prompt: Annotated[str, Field(description="Prompt", default="Draw a cat")]


@svg_drawer.post("/svgdrawer")
def draw_svg(data: SvgDrawerInput,  background_tasks: BackgroundTasks):
    result: Svg = SvgDrawer().draw(prompt=data.prompt)

    def remove_file(path: Path):
        path.unlink(missing_ok=True)

    with NamedTemporaryFile(suffix=".svg", delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        content = ElementTree.tostring(result.to_svg(), encoding="unicode")
        temp_path.write_text(content, encoding="utf-8")
        background_tasks.add_task(remove_file, temp_path)
        return  FileResponse(
            path=temp_path.as_posix(),
            filename=temp_path.name,
            media_type="image/svg+xml",
        )

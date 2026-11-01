from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, Field, field_validator
from starlette.responses import FileResponse

from app.libs.svg_drawer.v1.models.svg import Svg
from app.libs.svg_drawer.v1.svg_creator import SvgCreator

svg_drawer = APIRouter(tags=["svg-drawer"])


class SvgDrawerInput(BaseModel):
    prompt: Annotated[
        str,
        Field(description="Describe the SVG illustration", min_length=1, max_length=500),
    ]

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Prompt cannot be blank")
        return value


@svg_drawer.post("/svgdrawer")
def draw_svg(data: SvgDrawerInput, background_tasks: BackgroundTasks):
    result: Svg = SvgCreator().create(prompt=data.prompt)

    def remove_file(path: Path):
        path.unlink(missing_ok=True)

    with NamedTemporaryFile(suffix=".svg", delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_path.write_bytes(result.to_bytes())
        background_tasks.add_task(remove_file, temp_path)
        return FileResponse(
            path=temp_path.as_posix(),
            filename=temp_path.name,
            media_type="image/svg+xml",
        )

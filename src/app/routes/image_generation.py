"""Local FastAPI endpoint for generating images from text prompts."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

from app.services.image_generator import ImageGenerator, OpenAIImageGenerator

image_generation_router = APIRouter(prefix="/images", tags=["images"])
_image_generator = OpenAIImageGenerator()


def get_image_generator() -> ImageGenerator:
    """Return the configured backend; override this dependency to swap it."""
    return _image_generator


class ImageGenerationRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=32000)]
    size: str = Field(default="1024x1024", pattern=r"^\d{2,4}x\d{2,4}$")


@image_generation_router.post("/generate", response_class=FileResponse)
def generate_image(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    generator: ImageGenerator = Depends(get_image_generator),
) -> FileResponse:
    """Generate a PNG and return it as the response body."""
    # try:
    image_bytes = generator.generate(request.prompt, request.size)

    with NamedTemporaryFile(suffix=".png", delete=False) as image_file:
        image_path = Path(image_file.name)
        image_file.write(image_bytes)

    background_tasks.add_task(image_path.unlink, missing_ok=True)
    return FileResponse(
        path=image_path,
        filename="generated.png",
        media_type="image/png",
        background=background_tasks,
    )

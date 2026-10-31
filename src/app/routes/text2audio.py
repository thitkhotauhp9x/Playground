from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from gtts import gTTS
from tempfile import NamedTemporaryFile
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

text_2_audio_router = APIRouter(tags=["text2audio"])


class Text2Audio(BaseModel):
    text: Annotated[str, Field(default="Xin chào")]
    lang: Annotated[str, Field(default="vi")]



@text_2_audio_router.post("/text2audio")
def convert_text_to_audio(data: Text2Audio, background_tasks: BackgroundTasks):
    tts = gTTS(text=data.text, lang=data.lang)

    def remove_file(path: Path):
        path.unlink(missing_ok=True)

    with NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
        audio_path = Path(audio_file.name)
        tts.save(audio_path.name)

        background_tasks.add_task(remove_file, audio_path)
        return FileResponse(
            path=audio_path.name,
            filename=audio_path.name,
            media_type="audio/mpeg",
        )

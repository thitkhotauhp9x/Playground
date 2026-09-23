from pathlib import Path

from tests.english.text_to_audio_converter import text_to_audio


def test_text_to_audio() -> None:
    path = Path("output.mp3")

    text_to_audio("hello", "en", path.as_posix())
    path.exists()

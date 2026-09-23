from pathlib import Path

from gtts import gTTS


def text_to_audio(text: str, lang: str, output_path: str) -> None:
    tts_audio = gTTS(text=text, lang=lang, slow=False)
    tts_audio.save(output_path)


def test_text_to_audio() -> None:
    path = Path("output.mp3")

    text_to_audio("hello", "en", path.as_posix())
    path.exists()

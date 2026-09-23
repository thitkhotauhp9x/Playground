from gtts import gTTS


def text_to_audio(text: str, lang: str, output_path: str) -> None:
    tts_audio = gTTS(text=text, lang=lang, slow=False)
    tts_audio.save(output_path)

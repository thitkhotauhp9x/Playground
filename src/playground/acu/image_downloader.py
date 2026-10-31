from pathlib import Path
from urllib.parse import unquote

import requests


class ImageDownloader:
    @staticmethod
    def download(src: str, directory: Path) -> Path:
        response = requests.get(src, stream=True)
        image_name = unquote(Path(src).name)

        image_path = directory / image_name
        with open(image_path.as_posix(), "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path

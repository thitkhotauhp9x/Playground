from pathlib import Path
from bs4 import ResultSet, Tag
from app.libs.playground.acu import ImageDownloader


class MultipleImageDownloader:
    @staticmethod
    def download(elements: ResultSet[Tag], directory: Path) -> list[Path]:
        image_paths = []
        for element in elements:
            images = element.select("img")

            for image in images:
                image_src = image["src"]
                if image_src and isinstance(image_src, str):
                    image_path = ImageDownloader.download(image_src, directory)
                    image_paths.append(image_path)
        return image_paths

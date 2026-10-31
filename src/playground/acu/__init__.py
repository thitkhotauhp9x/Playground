from pathlib import Path

import requests
import bs4
from langchain_openai import ChatOpenAI
from jinja2 import Environment, FileSystemLoader

from playground.acu.image_downloader import ImageDownloader
from playground.acu.latex_converter import LatexConverter
from playground.acu.multiple_image_downloader import MultipleImageDownloader
from playground.executors.pdf_latex_executor import PdfLatexExecutor
from playground.parsers.acupuncture_point_output_parser import AcupuncturePointOutputParser

cwd = Path(__file__).parent
env = Environment(
    loader=FileSystemLoader(cwd),
    variable_start_string='<<',
    variable_end_string='>>'
)
TEMPLATE = env.get_template('main.ttex')

chat_model = ChatOpenAI(model="gpt-4o-mini")


def load_website(url: str) -> bs4.BeautifulSoup:
    response = requests.get(url)
    content = bs4.BeautifulSoup(response.content, "html.parser")
    if not content:
        raise ValueError("Cannot load the website")
    return content


def build_latex(point_code: str = "GB20"):
    content = TEMPLATE.render(tex_file=f"./{point_code}.tex")
    Path("main.tex").write_text(content)
    PdfLatexExecutor.execute("./main.tex", cwd=cwd)


def create_latex(point_code: str) -> None:
    url = f"https://www.mastertungacupuncture.org/acupuncture/traditional/points/{point_code}"
    content = load_website(url)
    field_items = content.select(".field-items")
    image_paths = MultipleImageDownloader.download(field_items, cwd)
    main_container = content.select_one(".page-flex-wrapper")

    output_parser = AcupuncturePointOutputParser(
        point_code=point_code,
        images=[path.name for path in image_paths],
    )

    latex_code = LatexConverter(chat_model=chat_model, output_parser=output_parser).convert(str(main_container))

    Path(f"{point_code}.tex").write_text(latex_code)
    build_latex(point_code)


def main():
    create_latex(point_code="GB21")


if __name__ == "__main__":
    main()

import subprocess
from pathlib import Path


class PdfLatexExecutor:
    @staticmethod
    def execute(tex_file: str, cwd: Path) -> None:
        command = f'docker run --rm -v "{cwd}:/workdir" -w /workdir texlive/texlive pdflatex {tex_file}'
        subprocess.run(command, shell=True, cwd=cwd)

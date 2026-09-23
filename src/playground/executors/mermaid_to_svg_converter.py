from playground.utils.temp import temp_file
from subprocess import run, PIPE


def convert_mermaid_to_svg(mermaid_code: str, output: str = "output.svg"):
    with temp_file() as tf:
        tf.write_text(mermaid_code, encoding="utf-8")
        return run(["mmdc", "-i", tf.as_posix(), "-o", output], check=True, stderr=PIPE)

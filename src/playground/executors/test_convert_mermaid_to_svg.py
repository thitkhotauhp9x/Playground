from subprocess import CalledProcessError

import pytest

from playground.executors.mermaid_to_svg_converter import convert_mermaid_to_svg
from playground.utils.temp import temp_file


@pytest.mark.parametrize(
    "code",
    [
        """stateDiagram-v2
    [*] --> Noun
    Noun --> Verb: "To agree"
    Noun --> Adjective: "Agreeable"
    Adjective --> Noun: "Agreeableness"
    Noun --> Adverb: "Agreeably"
    Verb --> Noun: "Agreement"
    Noun --> "Disagreement"
    "Disagreement" --> Noun: "Disagree"
"""
    ],
)
def test_convert_mermaid_to_svg(code):
    with temp_file(suffix=".svg") as svg_file:
        try:
            response = convert_mermaid_to_svg(code, svg_file.as_posix())
            print(response)
        except CalledProcessError as e:
            import pdb

            pdb.set_trace()
            print(e.stderr)
            pass

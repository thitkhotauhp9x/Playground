import textwrap


def check_understand(content: str) -> str:
    return f"""How do you understand this content?
{textwrap.indent(content, "> ", lambda line: True)}
"""

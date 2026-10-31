from pydantic import BaseModel
import textwrap
from typing_extensions import deprecated


@deprecated
class SystemTemplate(BaseModel):
    identity: str
    instructions: list[str]
    examples: list[str]

    def __str__(self) -> str:
        instructions = "\n".join(self.instructions)

        return SYSTEM_TEMPLATE.format(
            identity=self.identity,
            instructions=textwrap.indent(instructions, "* ", lambda line: True),
        )


SYSTEM_TEMPLATE = """# Identity
{identity}

# Instructions
{instructions}
# Examples
<assistance_input>
"""

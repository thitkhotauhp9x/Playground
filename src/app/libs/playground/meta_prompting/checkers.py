import textwrap

from langchain_core.messages import HumanMessage

from app.libs.playground.utils.openai_runner import llm


def check_understand(content: str):
    return llm.invoke(
        [
            HumanMessage(f"""How do you understand this content?
{textwrap.indent(content, "> ", lambda line: True)}
""")
        ]
    )

from langchain_core.messages import BaseMessage, HumanMessage
from rich.console import Console
from rich.markdown import Markdown

from app.libs.meta_prompting.creators.prompt_template_creator import (
    PromptTemplateCreator,
)


def test_draw_a_banana() -> None:
    console = Console(force_terminal=True)

    messages: list[BaseMessage] = [HumanMessage(content="Draw a banana.")]
    console.print(Markdown("# Create prompt template"))
    prompt_template_creator = PromptTemplateCreator()
    response = prompt_template_creator.create(messages)
    console.print(Markdown(response))

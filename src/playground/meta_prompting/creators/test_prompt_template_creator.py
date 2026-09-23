from langchain_core.messages import BaseMessage, HumanMessage
from rich.markdown import Markdown

from playground.meta_prompting.creators.prompt_template_creator import (
    PromptTemplateCreator,
)
from rich.console import Console


def test_draw_a_banana() -> None:
    console = Console(force_terminal=True)

    messages: list[BaseMessage] = [HumanMessage(content="Draw a banana.")]
    console.print(Markdown("# Create prompt template"))
    prompt_template_creator = PromptTemplateCreator()
    response = prompt_template_creator.create(messages)
    console.print(Markdown(response))

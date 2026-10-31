from functools import cached_property

from langchain_core.messages import BaseMessage, SystemMessage
from warnings import deprecated

from langchain_core.output_parsers import PydanticOutputParser

from app.libs.playground.meta_prompting.renders.markdown_prompt_template_renderer import (
    MarkdownPromptTemplateRenderer,
)
from app.libs.playground.utils.openai_runner import chat_model
from app.libs.playground.meta_prompting.models.prompt_template import PromptTemplate


class PromptTemplateCreator:
    def __init__(self) -> None:
        self._output_parser = PydanticOutputParser(pydantic_object=PromptTemplate)

    @cached_property
    def system_message(self) -> SystemMessage:
        prompt_template = PromptTemplate(
            identity="You are an export prompt engineer.",
            instructions=[
                f"""Help me design a prompt template for a given content."
{self._output_parser.get_format_instructions()}"""
            ],
            examples=[],
        )
        content = MarkdownPromptTemplateRenderer(prompt_template).render()
        return SystemMessage(content)

    def create(self, messages: list[BaseMessage]) -> str:
        chain = chat_model | self._output_parser

        prompt_template = chain.invoke(
            [
                self.system_message,
                *messages,
            ]
        )
        return MarkdownPromptTemplateRenderer(prompt_template).render()


@deprecated("Use PromptTemplateCreator() instead")
def design_prompt_template(messages: list[BaseMessage]) -> str:
    creator = PromptTemplateCreator()
    return creator.create(messages)

from langchain_core.messages import BaseMessage, HumanMessage
from rich.markdown import Markdown

from playground.meta_prompting.creators.form_creator import FormCreator
from playground.meta_prompting.creators.prompt_template_creator import (
    PromptTemplateCreator,
)
from playground.meta_prompting.models.data_entry import DataEntry
from rich.console import Console

from playground.utils.openai_runner import llm


def main() -> None:
    console = Console(force_terminal=True)

    messages: list[BaseMessage] = [HumanMessage(content="Draw a banana.")]
    console.print(Markdown("# Create prompt template"))
    prompt_template_creator = PromptTemplateCreator()
    response = prompt_template_creator.create(messages)
    console.print(Markdown(response))

    form_creator = FormCreator()

    form = form_creator.create(response)
    if form:
        console.print(Markdown("# Enter data entry"))
        data_entry = DataEntry(form)
        content = data_entry.enter()
        console.print(Markdown(content))
        human_message: HumanMessage = HumanMessage(content)
        messages.append(human_message)
    response = llm.invoke(messages)
    print(response)


if __name__ == "__main__":
    main()

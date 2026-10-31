import textwrap

from app.libs.playground.meta_prompting.models.prompt_template import PromptTemplate


class MarkdownPromptTemplateRenderer:
    def __init__(self, prompt_template: PromptTemplate) -> None:
        self._prompt_template = prompt_template

    def render_identity(self) -> str:
        if self._prompt_template.identity:
            return f"""# Identity
{self._prompt_template.identity}
"""
        return ""

    def render_instructions(self) -> str:
        if self._prompt_template.instructions:
            items: list[str] = ["# Instructions"]
            for index, item in enumerate(self._prompt_template.instructions):
                items.append(
                    f"{index + 1}. {textwrap.indent(item, '  ', lambda line: True).strip()}"
                )
            return "\n".join(items)
        return ""

    def render_examples(self) -> str:
        if self._prompt_template.examples:
            items: list[str] = ["# Examples"]
            for index, item in enumerate(self._prompt_template.examples):
                items.append(f"""## Example {index + 1}
<user_query>
{item.user_query}
</user_query>

<assistance_response>
{item.assistance_response}
</assistance_response>
""")
            return "\n".join(items)
        return ""

    def render(self) -> str:
        return f"""{self.render_identity()}

{self.render_instructions()}

{self.render_examples()}
"""

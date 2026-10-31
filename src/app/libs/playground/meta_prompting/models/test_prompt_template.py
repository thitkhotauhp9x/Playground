from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser

from app.libs.playground.meta_prompting.checkers import check_understand
from app.libs.playground.meta_prompting.models.prompt_template import PromptTemplate
from app.libs.playground.utils.openai_runner import llm


def test_draw_a_banana():
    output_parser = PydanticOutputParser(pydantic_object=PromptTemplate)

    response = llm.invoke(
        [
            HumanMessage(f"""Create a prompt template to draw a banana.
{output_parser.get_format_instructions()}
""")
        ]
    )
    print(response)


def test_checker():
    output_parser = PydanticOutputParser(pydantic_object=PromptTemplate)
    response = check_understand(output_parser.get_format_instructions())
    print(response)

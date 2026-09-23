from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from warnings import deprecated

from playground.meta_prompting.models.form import Form
from playground.meta_prompting.models.null_form import NullForm
from playground.templates.function_output_parser import indent
from playground.utils.openai_runner import chat_model


class FormCreator:
    def __init__(self) -> None:
        self._output_parser = PydanticOutputParser(pydantic_object=Form)
        self._llm = _llm = chat_model | self._output_parser

    def create(self, openai_response: str) -> Form:
        return self._llm.invoke(
            [
                SystemMessage(f"""You are a form designer.
Nhiệm vụ của bạn là xác định xem phản hồi từ OpenAI cần thu thập dữ liệu nào từ người dùng hay không.
* Nếu cần thu thập yêu cầu từ người dùng thì thiết kế một biểu mẫu để làm việc trên.
  {indent(self._output_parser.get_format_instructions(), "  ")}
* Nếu không cần thu thuật dữ liệu nào từ người dùng thì trả về null form với nội dung như sau
 {NullForm().model_dump_json(indent=2)}
"""),
                HumanMessage(f"""This is a OpenAI response:
<openai_response>
{openai_response}
</openai_response>
"""),
            ]
        )


@deprecated("Use FormCreator().create instead")
def create_form(openai_response: str) -> Form:
    creator = FormCreator()
    return creator.create(openai_response)

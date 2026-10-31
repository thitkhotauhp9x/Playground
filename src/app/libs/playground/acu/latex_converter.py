from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import BaseOutputParser


class LatexConverter:
    def __init__(self, chat_model: BaseChatModel, output_parser: BaseOutputParser):
        self._model: BaseChatModel = chat_model
        self._output_parser: BaseOutputParser = output_parser

    def convert(self, content: str) -> str:
        human_query = HumanMessage(f"""Chuyển đổi nội dung sau sang latex (Nhớ translate thành tiếng việt,\
 tên huyệt vị và kinh lạc cũng cần chuyển sang tiếng Việt)
```text
{content}
```

{self._output_parser.get_format_instructions()}
""")
        llm = self._model | self._output_parser
        return llm.invoke([human_query])

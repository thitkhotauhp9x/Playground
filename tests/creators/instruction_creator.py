from langchain_core.messages import HumanMessage, SystemMessage

from app.libs.playground.utils.dort import dort
from app.libs.playground.utils.openai_runner import llm_invoke


class InstructionCreator:
    def __init__(self, prompt: str) -> None:
        self._prompt: str = prompt

    @llm_invoke
    def create(self):
        return [
            SystemMessage("""Bạn là một chuyên gia kỹ thuật AI và thiết kế Prompt (Prompt Engineer).
Nhiệm vụ của bạn là viết các hướng dẫn chi tiết, rõ ràng để yêu cầu các mô hình ngôn ngữ lớn (như GPT) \
thực hiện một nhiệm vụ cụ thể dựa trên ý tưởng gốc."""),
            HumanMessage(f"""Yêu cầu gốc của tôi:
> {self._prompt}\
"""),
        ]


create_instruction = dort(lambda query: InstructionCreator(query).create())


human = dort(HumanMessage)
system = dort(SystemMessage)

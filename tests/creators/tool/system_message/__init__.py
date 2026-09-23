from langchain_core.messages import HumanMessage

from tests.creators.tool.system_message.structured_system_message import (
    StructuredSystemMessage,
    SSM_OUTPUT_PARSER,
)

from playground.utils.dort import dort
from playground.utils.openai_runner import llm_invoke, lst


@dort(SSM_OUTPUT_PARSER.invoke)
@llm_invoke
@lst
def create(requirements: str):
    yield StructuredSystemMessage(
        identity="You are an automatic prompt engineer",
        instructions=f"Create the system message based on user requirements.\n {SSM_OUTPUT_PARSER.get_format_instructions()}",
    ).to_message()
    yield HumanMessage(
        content=f"""This is user requirements:
{requirements}
"""
    )


def main():
    response = create(
        """Tôi sẽ nhập vào hai số, nhiệm vụ của bạn là trả về cho tôi kết quả của tổng hai số"""
    )
    result = response.query("2 + x")
    print(result)


if __name__ == "__main__":
    main()

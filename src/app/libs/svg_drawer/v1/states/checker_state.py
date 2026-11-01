from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown

from app.libs.loggers import get_logger
from app.libs.svg_drawer.v1.design_rules import DESIGN_RULES
from app.libs.svg_drawer.v1.models.graph_state import GraphState

logger = get_logger(__name__)

console = Console(force_terminal=True)


class BaseResponse(BaseModel):
    reasoning: Annotated[
        str,
        Field(
            description="Step-by-step reasoning or thought process used to arrive "
            "at the final result. "
            "Always generate this first.\n"
            "CRITICAL: Do NOT assume, extrapolate, or invent any missing input values"
            " or contextual facts."
            "Work STRICTLY with the provided inputs."
            "If required inputs are missing or ambiguous, state the exact missing information"
            " here and fail "
            "gracefully by returning an error."
        ),
    ]
    error: Annotated[
        str | None,
        Field(
            description="An error message if the result cannot be inferred due to invalid inputs,"
            " missing context, "
            "or logical issues. Must be explicit JSON null (not 'null' as string) "
            "if operation is successful."
        ),
    ]


class ImproveResponse(BaseResponse):
    improved_user_prompt: Annotated[
        str,
        Field(
            description="Nếu không đúng ý định bạn vẽ thì cần update."
            "Mô tả chi tiết cần bổ sung thêm các shape nào, kích thước ra sao."
        ),
    ]
    isOk: Annotated[
        bool,
        Field(
            description="Nếu đúng như ý định bạn vẽ rồi thì giá trị này bằng True."
            "Nếu không giá trị này bằng False"
        ),
    ]


def check(state: GraphState) -> GraphState:
    logger.info("CHECKING SVG")
    output_parser = PydanticOutputParser(pydantic_object=ImproveResponse)
    chain = state.chat_model
    message_content = f"""Đây là ảnh svg bạn vẽ:
```svg
{state.svg.to_bytes().decode("utf-8")}
```

Đây là yêu cầu từ người dùng:

```userPrompt
{state.design[-1]}
```

Kiểm tra xem ảnh svg đã đáp ứng yêu cầu từ người dùng chưa.
Đánh giá thêm theo các quy tắc sau; chỉ đặt isOk=true khi chủ thể dễ nhận ra, bố cục
cân đối, tỉ lệ hợp lý, màu và nét nhất quán, không có phần bị cắt:
{DESIGN_RULES}
{output_parser.get_format_instructions()}\
"""
    console.print(Markdown(message_content))
    messages = [HumanMessage(content=message_content)]
    state.history += messages
    response = chain.invoke(messages)
    state.history.append(response)
    console.print(Markdown(StrOutputParser().invoke(response)))

    pydantic_obj = output_parser.invoke(response)
    state.isDone = pydantic_obj.isOk
    state.design.append(pydantic_obj.improved_user_prompt)
    # logger.debug(state.model_dump_json(indent=2))
    return state

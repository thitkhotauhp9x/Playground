from typing import Annotated
from xml.etree import ElementTree

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from app.libs.svg_drawer.v1.models.graph_state import GraphState


class ImproveResponse(BaseModel):
    updatedPrompt: Annotated[
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
    reasoning: str


def check(state: GraphState) -> GraphState:
    output_parser = PydanticOutputParser(pydantic_object=ImproveResponse)
    content = ElementTree.tostring(state.svg.to_svg(), encoding="utf-8")
    chain = state.chat_model
    messages = [
        HumanMessage(
            content=f"""Đây là ảnh svg bạn vẽ
```svg
{content.decode("utf-8")}
```
Đây là yêu cầu từ người dùng:
```userPrompt
{state.prompt}
```

Đánh giá ảnh svg bạn vẽ so với yêu cầu của người dùng.
Nếu không đúng như ý định bạn vẽ hãy cải thiện lại designPrompt để
có thể vẽ như gì bạn muốn. {output_parser.get_format_instructions()}

```designPrompt
{state.design[-1]}
```
"""
        )
    ]
    state.history += messages
    response = chain.invoke(messages)
    state.history.append(response)

    pydantic_obj = output_parser.invoke(response)
    state.isDone = pydantic_obj.isOk
    state.design.append(pydantic_obj.updatedPrompt)
    return state

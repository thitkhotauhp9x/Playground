from dataclasses import dataclass
from typing import Annotated
from xml.etree import ElementTree

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain.agents import create_agent
from langchain.messages import SystemMessage
from pydantic import BaseModel, Field

from app.libs.svg_drawer.models.shapes.circle import Circle
from app.libs.svg_drawer.models.shapes.eclipse import Eclipse
from app.libs.svg_drawer.models.shapes.line import Line
from app.libs.svg_drawer.models.shapes.rect import Rect
from app.libs.svg_drawer.models.svg import Svg

CHAT_MODEL = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SvgDrawerState(BaseModel):
    prompt: str
    design: list[str]
    svg: Svg | None = None


def draw_svg(state: SvgDrawerState) -> SvgDrawerState:
    tools = [
        Line, Circle, Eclipse, Rect
    ]
    agent_executor = create_agent(CHAT_MODEL, tools, response_format=Svg, system_prompt=SystemMessage(content=f"""\
Bạn là chuyên gia về svg nhiệm vụ của bạn là nhận prompt và tạo ảnh svg.
Làm từng bước một đến khi tạo thành một hình ảnh hoàn chỉnh đẩy đủ các chi tiết.
"""))
    response = agent_executor.invoke({"messages": [
        HumanMessage(content=state.design[-1])]})

    state.svg = response["structured_response"]
    state.svg.display()
    return state

class ImproveResponse(BaseModel):
    updatedPrompt: Annotated[str | None, Field(description="Nếu không đúng ý định bạn vẽ thì cần update prompt.")]
    isOk: Annotated[bool, Field(description="Nếu đúng như ý định bạn vẽ rồi thì giá trị này bằng True. Nếu không giá trị này bằng False")]
    reasoning: str

def improve(state: SvgDrawerState) -> ImproveResponse:
    output_parser = PydanticOutputParser(pydantic_object=ImproveResponse)
    content = ElementTree.tostring(state.svg.to_svg(), encoding="unicode")
    chain = CHAT_MODEL | output_parser
    response = chain.invoke([HumanMessage(content=f"""Đây là ảnh svg bạn vẽ
```svg
{content}
```
Đây là yêu cầu từ người dùng:
```userPrompt
{state.prompt}
```

Đánh giá ảnh svg bạn vẽ so với yêu cầu của người dùng.
Nếu không đúng như ý định bạn vẽ hãy cải thiện lại designPrompt để
có thể vẽ như gì bạn muốn. {output_parser.get_format_instructions()}
```designPrompt
{state.design}
```
""")])
    state.design = response.updatedPrompt
    return response.isOk


@dataclass
class SvgDrawer:
    def draw(self, prompt: str):
        builder = StateGraph(SvgDrawerState)
        builder.add_node("draw_svg", draw_svg)
        builder.add_node("improve", improve)

        builder.set_entry_point("draw_svg")
        builder.add_conditional_edges(
            "draw_svg",  # Từ node 'checker'
            improve,  # Hàm kiểm tra điều kiện
            {
                True: END,
                False: "draw_svg",
            },  # Bản đồ ánh xạ kết quả ra tên node
        )
        # builder.add_edge("draw_svg", "checker")
        graph = builder.compile()
        output = graph.invoke(SvgDrawerState(prompt=prompt, svg=None, design=[prompt]))
        svg = output["svg"]
        return svg

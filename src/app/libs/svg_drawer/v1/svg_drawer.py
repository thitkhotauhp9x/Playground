from dataclasses import dataclass
from typing import Annotated
from xml.etree import ElementTree

from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.shapes.eclipse import Eclipse
from app.libs.svg_drawer.v1.models.shapes.line import Line
from app.libs.svg_drawer.v1.models.shapes.rect import Rect
from app.libs.svg_drawer.v1.models.svg import Svg

CHAT_MODEL = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SvgDrawerState(BaseModel):
    prompt: str
    design: list[str]
    svg: Svg = Svg()
    isDone: bool = False


def draw_svg(state: SvgDrawerState) -> SvgDrawerState:

    @tool
    def draw_line(line_id: str, x1: float | int, x2: float | int, y1: float | int, y2: float | int):
        """
        Draw a line
        Args:
            line_id: Mã định danh của đoạn thẳng
            x1: Toạ độ x điểm bắt đầu
            x2: Toạ độ x điểm kết thúc
            y1: Toạ độ y điểm bắt đầu
            y2: Toạ độ y điểm kết thúc

        Returns: None

        """
        line = Line(id=line_id, x1=x1, x2=x2, y1=y1, y2=y2)
        state.svg.shapes.append(line)

    @tool
    def draw_circle(circle_id: str, r, cx, cy, fill):
        """
        Draw a circle
        Args:
            circle_id: mã định danh của đường tròn
            r: Bán kính hình tròn
            cx: Toạ độ tâm x
            cy: Toạ độ tâm y
            fill: Màu sắc tô nền

        Returns: None
        """
        circle = Circle(id=circle_id, r=r, cx=cx, cy=cy, fill=fill)
        state.svg.shapes.append(circle)

    @tool
    def draw_eclipse(eclipse_id, rx, ry, cx, cy, fill):
        """
        Draw a eclipse
        Args:
            eclipse_id: Mã định danh của hình eclipse
            rx: Bán kính hình elip theo trục x
            ry: Bán kính hình elip theo trục y
            cx: Toạ độ tâm x
            cy: Toạ độ tâm y
            fill: Màu sắc tô nền

        Returns: None
        """
        eclipse = Eclipse(id=eclipse_id, rx=rx, ry=ry, cx=cx, cy=cy, fill=fill)
        state.svg.shapes.append(eclipse)

    @tool
    def draw_rect(rect_id, width, height, x, y, rx, ry, fill):
        """
        Draw a rect
        Args:
            rect_id: Mã định danh của hình chữ nhật
            width: Required. The width of the rectangle
            height: Required. The height of the rectangle
            x: The x-position for the top-left corner of the rectangle
            y: The y-position for the top-left corner of the rectangle
            rx: The x radius of the corners of the rectangle
             (used to round the corners). Default is 0
            ry: The y radius of the corners of the rectangle
             (used to round the corners). Default is 0
            fill: Màu sắc tô nền

        Returns: None

        """
        rect = Rect(id=rect_id, width=width, height=height, x=x, y=y, rx=rx, ry=ry, fill=fill)
        state.svg.shapes.append(rect)

    tools = [draw_line, draw_circle, draw_eclipse, draw_rect]
    svg_code = ElementTree.tostring(state.svg.to_svg(), encoding="utf-8")
    agent_executor = create_agent(
        CHAT_MODEL,
        tools,
        system_prompt=SystemMessage(
            content=f"""\
Đây là ảnh svg đã vẽ hãy gọi từng tool một để thực hiện chỉnh sửa ảnh svg này\
 sao cho đúng yêu cầu của người dùng.
Nếu shape đã có trong ảnh svg rồi thì đừng vẽ lại nữa.
```svg
{svg_code.decode("utf-8")}
```
"""
        ),
    )
    agent_executor.invoke({"messages": [HumanMessage(content=state.design[-1])]})
    state.svg.display()
    return state


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


def check(state: SvgDrawerState) -> SvgDrawerState:
    output_parser = PydanticOutputParser(pydantic_object=ImproveResponse)
    content = ElementTree.tostring(state.svg.to_svg(), encoding="utf-8")
    chain = CHAT_MODEL | output_parser
    response = chain.invoke(
        [
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
    )
    state.isDone = response.isOk
    state.design.append(response.updatedPrompt)
    return state


def is_done(state: SvgDrawerState) -> bool:
    return state.isDone


@dataclass
class SvgDrawer:
    def draw(self, prompt: str):
        builder = StateGraph(SvgDrawerState)
        builder.add_node("draw_svg", draw_svg)
        builder.add_node("check", check)

        builder.set_entry_point("draw_svg")
        builder.add_edge("draw_svg", "check")

        builder.add_conditional_edges(
            "check",  # Từ node 'checker'
            is_done,  # Hàm kiểm tra điều kiện
            {
                True: END,
                False: "draw_svg",
            },  # Bản đồ ánh xạ kết quả ra tên node
        )
        # builder.add_edge("draw_svg", "checker")
        graph = builder.compile()
        output = graph.invoke(SvgDrawerState(prompt=prompt, svg=Svg(), design=[prompt]))
        svg = output["svg"]
        return svg

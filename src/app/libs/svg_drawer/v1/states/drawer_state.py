from xml.etree import ElementTree

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool

from app.libs.loggers import get_logger
from app.libs.svg_drawer.v1.design_rules import DESIGN_RULES
from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.svg_drawer import SvgDrawer

logger = get_logger(__name__)


def draw_svg(state: GraphState) -> GraphState:
    logger.info("DRAWING SVG")
    drawer = SvgDrawer(state.svg)

    tools = [
        StructuredTool.from_function(func=drawer.draw_line),
        StructuredTool.from_function(func=drawer.draw_circle),
        StructuredTool.from_function(func=drawer.draw_eclipse),
        StructuredTool.from_function(func=drawer.draw_rect),
        StructuredTool.from_function(func=drawer.draw_path),
        StructuredTool.from_function(func=drawer.delete_shape),
    ]
    svg_code = ElementTree.tostring(state.svg.to_svg(), encoding="utf-8")
    agent_executor = create_agent(
        state.chat_model,
        tools,
        system_prompt=SystemMessage(
            content=f"""\
Bạn là họa sĩ minh họa vector. Hãy dùng các tool để tạo/chỉnh SVG theo prompt mới nhất.
Tạo bố cục có chủ thể rõ ràng, dùng tọa độ trong khung 300 x 200. Vẽ từng shape cần
thiết, ưu tiên ít shape có chủ đích; không vẽ lặp các shape đã có.

{DESIGN_RULES}

SVG hiện tại:
```svg
{svg_code.decode("utf-8")}
```
"""
        ),
    )
    state.history.append(HumanMessage(content=state.design[-1]))

    response = agent_executor.invoke({"messages": state.history})
    state.history += response["messages"]
    return state

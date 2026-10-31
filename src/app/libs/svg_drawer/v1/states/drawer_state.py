from xml.etree import ElementTree

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool

from app.libs.loggers import get_logger
from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.svg_drawer import SvgDrawer

logger = get_logger(__name__)


def draw_svg(state: GraphState) -> GraphState:
    drawer = SvgDrawer(state)

    tools = [
        StructuredTool.from_function(func=drawer.draw_line),
        StructuredTool.from_function(func=drawer.draw_circle),
        StructuredTool.from_function(func=drawer.draw_eclipse),
        StructuredTool.from_function(func=drawer.draw_rect),
    ]
    svg_code = ElementTree.tostring(state.svg.to_svg(), encoding="utf-8")
    agent_executor = create_agent(
        state.chat_model,
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
    state.history.append(HumanMessage(content=state.design[-1]))

    response = agent_executor.invoke({"messages": state.history})
    state.history += response["messages"]
    logger.debug(state.model_dump_json(indent=2))
    state.svg.display()
    return state

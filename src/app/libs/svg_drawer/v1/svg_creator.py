from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph

from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.models.svg import Svg
from app.libs.svg_drawer.v1.states.checker_state import check
from app.libs.svg_drawer.v1.states.drawer_state import draw_svg

CHAT_MODEL = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class SvgCreator:
    @staticmethod
    def create(prompt: str):
        builder = StateGraph(GraphState)
        builder.add_node("draw", draw_svg)
        builder.add_node("check", check)

        builder.set_entry_point("draw")
        builder.add_edge("draw", "check")

        def is_done(state: GraphState) -> bool:
            return state.isDone

        builder.add_conditional_edges(
            "check",
            is_done,
            {
                True: END,
                False: "draw",
            },
        )
        graph = builder.compile()
        output = graph.invoke(
            GraphState(prompt=prompt, svg=Svg(), design=[prompt], chat_model=CHAT_MODEL)
        )
        svg = output["svg"]
        return svg

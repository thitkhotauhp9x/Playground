from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from app.libs.svg_drawer.v2.models.blueprint_response import BlueprintResponse
from app.libs.svg_drawer.v2.models.graph_state import GraphState
from app.libs.svg_drawer.v2.models.svg_response import SVGResponse


# Node 1: Chuyển đổi prompt thành bản thiết kế (Blueprint)
def create_blueprint_node(state: GraphState):
    query = state.query
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
    structured_llm = llm.with_structured_output(BlueprintResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Bạn là một chuyên gia kiến trúc đồ họa vector."
                "Nhiệm vụ của bạn là chuyển đổi câu lệnh đơn giản"
                "của người dùng thành một bản thiết kế cấu trúc chi tiết"
                "(blueprint) bao gồm: kích thước khung vẽ, tọa độ các thành phần"
                "(thân, cuống, lá, bóng đổ), và mã màu HEX cụ thể.",
            ),
            ("human", "Hãy tạo bản thiết kế chi tiết cho đối tượng: {query}"),
        ]
    )

    result = (prompt | structured_llm).invoke({"query": query})
    print("[Node 1 - Blueprint]: Đã tạo thành công bản thiết kế cấu trúc.")
    if not isinstance(result, BlueprintResponse):
        raise TypeError("The object is not BlueprintResponse")
    print(result.blueprint_text)
    return {"blueprint_query": result.blueprint_text}


# Node 2: Dựa vào blueprint để sinh mã SVG chi tiết
def generate_svg_node(state: GraphState):
    blueprint = state.blueprint_query
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    structured_llm = llm.with_structured_output(SVGResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Bạn là chuyên gia thiết kế SVG."
                "Dựa hoàn toàn vào bản thiết kế chi tiết (blueprint)"
                "được cung cấp bên dưới,"
                "hãy viết mã XML chuẩn bắt đầu bằng thẻ <svg> và kết thúc bằng </svg>.",
            ),
            ("human", "Bản thiết kế chi tiết: {blueprint}"),
        ]
    )

    result = (prompt | structured_llm).invoke({"blueprint": blueprint})
    print("[Node 2 - SVG Generator]: Đã tạo xong mã vector từ blueprint.")
    if not isinstance(result, SVGResponse):
        raise TypeError("The object is not SVGResponse")
    return {"svg_code": result.svg_code}


# Node 3: Lưu tệp SVG xuống đĩa
def save_svg_node(state: GraphState):
    file_name = "apple_blueprint_graph.svg"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(state.svg_code)
    print(f"[Node 3 - Saver]: Đã lưu thành công tệp {file_name}!")
    return {}


def main():
    # Xây dựng đồ thị quy trình LangGraph
    workflow = StateGraph(GraphState)

    workflow.add_node("create_blueprint", create_blueprint_node)
    workflow.add_node("generate_svg", generate_svg_node)
    workflow.add_node("save_svg", save_svg_node)

    workflow.add_edge(START, "create_blueprint")
    workflow.add_edge("create_blueprint", "generate_svg")
    workflow.add_edge("generate_svg", "save_svg")
    workflow.add_edge("save_svg", END)

    app = workflow.compile()

    app.invoke(GraphState(query="draw an apple", blueprint_query="", svg_code=""))


if __name__ == "__main__":
    main()

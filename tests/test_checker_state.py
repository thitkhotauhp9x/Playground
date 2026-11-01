from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.svg import Svg
from app.libs.svg_drawer.v1.states.checker_state import check
from app.libs.svg_drawer.v1.svg_creator import CHAT_MODEL


def test_checker_state():
    state = GraphState(
        prompt="Draw a circle",
        design=["Draw a circle"],
        chat_model=CHAT_MODEL,
    )
    response = check(state)
    assert not response.isDone


def test_checker_state_with_chat_model():
    state = GraphState(
        prompt="Draw a circle",
        design=["Draw a circle"],
        chat_model=CHAT_MODEL,
        svg=Svg(
            shapes=[
                Circle(shape_type="circle", shape_id="circle1", r=50, cx=150, cy=100, fill="blue")
            ]
        ),
    )
    response = check(state)
    assert response.isDone

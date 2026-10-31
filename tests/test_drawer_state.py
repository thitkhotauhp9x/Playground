from app.libs.svg_drawer.v1.models.graph_state import GraphState
from app.libs.svg_drawer.v1.models.shapes.circle import Circle
from app.libs.svg_drawer.v1.models.shapes.ellipse import Ellipse
from app.libs.svg_drawer.v1.models.shapes.line import Line
from app.libs.svg_drawer.v1.models.shapes.rect import Rect
from app.libs.svg_drawer.v1.states.drawer_state import draw_svg
from app.libs.svg_drawer.v1.svg_creator import CHAT_MODEL


def test_draw_a_circle():
    prompt = (
        "Please draw a blue circle with a radius of 50 pixels, centered "
        "at coordinates x=150 and y=100, and assign it the ID 'circle1'."
    )
    state = GraphState(prompt=prompt, design=[prompt], chat_model=CHAT_MODEL)

    state = draw_svg(state)
    assert state.svg.shapes == [
        Circle(shape_type="circle", id="circle1", r=50, cx=150, cy=100, fill="blue")
    ]


def test_draw_a_rectangle():
    prompt = (
        "Please draw a blue rectangle with a width of 100 pixels, a height "
        "of 50 pixels, positioned at coordinates x=50 and y=75, with sharp "
        "corners (rx=0, ry=0), and assign it the ID 'rect1'."
    )
    state = GraphState(prompt=prompt, design=[prompt], chat_model=CHAT_MODEL)

    state = draw_svg(state)
    assert state.svg.shapes == [
        Rect(
            shape_type="rect", id="rect1", width=100, height=50, x=50, y=75, rx=0, ry=0, fill="blue"
        )
    ]


def test_draw_a_ellipse():
    prompt = (
        "Please draw a blue ellipse with a horizontal "
        "radius of 50 pixels, a vertical radius of 30 "
        "pixels, centered at coordinates x=150 and y=100, "
        "and assign it the ID 'eclipse1'."
    )
    state = GraphState(prompt=prompt, design=[prompt], chat_model=CHAT_MODEL)

    state = draw_svg(state)
    assert state.svg.shapes == [
        Ellipse(shape_type="ellipse", rx=50, ry=30, cx=150, cy=100, fill="blue", id="eclipse1")
    ]


def test_draw_a_line():
    prompt = ("Please draw a line starting from coordinates x=0, y=0 to x=300, y=0,"
              " and assign it the ID 'line1'.")
    state = GraphState(prompt=prompt, design=[prompt], chat_model=CHAT_MODEL)

    state = draw_svg(state)
    assert state.svg.shapes == [Line(shape_type="line", id="line1", x1=0, y1=0, x2=300, y2=0)]

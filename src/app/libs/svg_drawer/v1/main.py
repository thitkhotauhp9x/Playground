import dspy

from app.libs.loggers import get_logger
from app.libs.svg_drawer.v1.models.svg import Svg
from app.libs.svg_drawer.v1.svg_drawer import SvgDrawer

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))


logger = get_logger(__name__)


def main():
    logger.info("DRAWING SVG")
    svg = Svg()
    drawer = SvgDrawer(svg=svg)

    agent = dspy.RLM(
        "context, question -> answer",
        tools=[
            drawer.draw_line,
            drawer.draw_circle,
            drawer.draw_eclipse,
            drawer.draw_rect,
            drawer.draw_path,
            drawer.delete_shape,
        ],
        max_iters=2,
    )
    result = agent(question="Draw a circle", context="Draw a svg image by using tools")
    print(result)
    print(agent)
    svg.display()


if __name__ == "__main__":
    main()

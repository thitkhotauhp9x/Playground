from typing import List
from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

from app.libs.svg_drawer.draw_iamge import generate_random_points_ordered_by_time


class Point(BaseModel):
    x: float
    y: float


class Polygon(BaseModel):
    points: list[Point] = Field(
        description=(
            "List of 2D coordinates representing the adjusted polygon vertices"
        )
    )


def adjust_polygon(prompt: str, initial_points: list[tuple]) -> list[tuple]:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(Polygon)

    formatted_points = [{"x": p[0], "y": p[1]} for p in initial_points]

    system_prompt = (
        "You are a precise geometric transformation engine. Modify the given"
        " polygon vertices based on the user prompt to form the requested shape"
        " while preserving sequential vertex order."
    )

    user_message = (
        f"Transformation Prompt: {prompt}\nInitial Vertices:"
        f" {formatted_points}\nReturn the adjusted set of points."
    )

    result = structured_llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )

    return [(p.x, p.y) for p in result.points]


def plot_polygons(initial: list[tuple], adjusted: list[tuple]):
    init_closed = initial + [initial[0]]
    adj_closed = adjusted + [adjusted[0]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot 1: Trước khi hiệu chỉnh
    ax1.plot(
        [p[0] for p in init_closed],
        [p[1] for p in init_closed],
        "r--o",
        linewidth=2,
    )
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax1.axvline(0, color="gray", linewidth=0.5, linestyle="--")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.set_title("Trước khi hiệu chỉnh (Initial)")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_aspect("equal", adjustable="box")

    # Plot 2: Sau khi hiệu chỉnh
    ax2.plot(
        [p[0] for p in adj_closed],
        [p[1] for p in adj_closed],
        "b-o",
        linewidth=2,
    )
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle="--")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle="--")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.set_title("Sau khi hiệu chỉnh (Adjusted)")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_aspect("equal", adjustable="box")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    initial = generate_random_points_ordered_by_time(n=200, noise_level=0.5)
    # sample_points = [(0, 0), (4, 0), (4, 4), (0, 4)]
    prompt_text = "Điều chỉnh lại vị trí các điểm này để tạo thành hình quả táo."
    adjusted = adjust_polygon(prompt_text, initial)
    print("Adjusted Points:", adjusted)
    plot_polygons(initial, adjusted)

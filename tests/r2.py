from typing import List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Point(BaseModel):
  x: float
  y: float


class Polygon(BaseModel):
  points: List[Point] = Field(
      description="List of 2D coordinates representing the adjusted polygon vertices"
  )


def adjust_polygon(prompt: str, initial_points: List[tuple]) -> List[tuple]:
  llm = ChatOpenAI(model="gpt-4o", temperature=0)
  structured_llm = llm.with_structured_output(Polygon)

  formatted_points = [{"x": p[0], "y": p[1]} for p in initial_points]

  system_prompt = (
      "You are a precise geometric transformation engine. Modify the given "
      "polygon vertices based on the user prompt to form the requested shape "
      "while preserving sequential vertex order."
  )

  user_message = (
      f"Transformation Prompt: {prompt}\n"
      f"Initial Vertices: {formatted_points}\n"
      "Return the adjusted set of points."
  )

  result = structured_llm.invoke([
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_message},
  ])

  return [(p.x, p.y) for p in result.points]


# Example execution:
if __name__ == "__main__":
  initial = [(0, 0), (4, 0), (4, 4), (0, 4)]
  prompt_text = (
      "Curve the top edge outward into a dome shape by adding 3 intermediate"
      " points"
  )
  adjusted = adjust_polygon(prompt_text, initial)
  print("Adjusted Points:", adjusted)
from pydantic import BaseModel


class GraphState(BaseModel):
    query: str
    blueprint_query: str
    svg_code: str

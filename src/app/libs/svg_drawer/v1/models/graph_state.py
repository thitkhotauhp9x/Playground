from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AnyMessage
from pydantic import BaseModel

from app.libs.svg_drawer.v1.models.svg import Svg


class GraphState(BaseModel):
    prompt: str
    design: list[str]
    svg: Svg = Svg()
    isDone: bool = False
    chat_model: BaseChatModel
    history: list[AnyMessage] = []

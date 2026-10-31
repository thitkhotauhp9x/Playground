from abc import ABC, abstractmethod
from typing import Annotated
from xml.etree.ElementTree import Element

from pydantic import BaseModel, Field


class Shape(BaseModel, ABC):
    shape_id: Annotated[str, Field(alias="id", description="Mã định danh ID của shape")]

    @abstractmethod
    def to_svg(self) -> Element:
        pass

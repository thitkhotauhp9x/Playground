from abc import ABC, abstractmethod

from pydantic import BaseModel


class BasePathData(BaseModel, ABC):
    @abstractmethod
    def to_svg_string(self) -> str:
        pass

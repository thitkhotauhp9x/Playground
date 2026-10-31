from pydantic import BaseModel, Field


class SVGResponse(BaseModel):
    svg_code: str = Field(description="Mã SVG XML hoàn chỉnh")

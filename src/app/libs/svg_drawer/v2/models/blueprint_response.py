from pydantic import BaseModel, Field


class BlueprintResponse(BaseModel):
    blueprint_text: str = Field(
        description="Bản thiết kế chi tiết bao gồm kích thước khung vẽ,"
        " tọa độ các phần, và mã màu HEX"
    )

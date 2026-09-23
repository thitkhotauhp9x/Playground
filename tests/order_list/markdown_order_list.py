from pydantic import BaseModel

from hat.playground.models.order_list.order_list import OrderList


class MarkdownOrderList(BaseModel):
    order_list: OrderList

    def to_markdown(self) -> str:
        content = ""
        for index, item in enumerate(self.order_list.items):
            content += f"- Step {index + 1}: {item.description}\n"
        return content

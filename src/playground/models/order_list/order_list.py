from pydantic import BaseModel

from hat.playground.models.order_list.base_item import BaseItem


class OrderList(BaseModel):
    items: list[BaseItem]

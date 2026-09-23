from playground.models.order_list.base_item import BaseItem
from playground.models.order_list.markdown_order_list import MarkdownOrderList
from playground.models.order_list.order_list import OrderList


def main():
    first_list = OrderList(
        items=[
            BaseItem(description="Step 1"),
            BaseItem(description="Step 2"),
            BaseItem(description="Step 3"),
        ]
    )

    print(MarkdownOrderList(order_list=first_list).to_markdown())


if __name__ == "__main__":
    main()

from app.libs.playground.models import BaseItem
from app.libs.playground.models import MarkdownOrderList
from app.libs.playground.models import OrderList


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

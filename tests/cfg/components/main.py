import inspect
from typing import List, Optional
from collections.abc import Callable

from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from app.libs.playground.utils.openai_runner import llm_invoke


class CFGNode(BaseModel):
    """Class cơ sở đại diện cho một nút trong Đồ thị dòng điều khiển (CFG)."""

    node_id: str = Field(..., description="Mã định danh của nút")
    description: str = Field(default="", description="Mô tả nút")
    next_node_ids: list[str] = Field(
        default_factory=list, description="Danh sách ID các nút tiếp theo"
    )

    def add_next(self, node: "CFGNode") -> None:
        """Thêm ID nút tiếp theo trong dòng điều khiển."""
        self.next_node_ids.append(node.node_id)


class StartNode(CFGNode):
    """Điểm bắt đầu của đơn vị chương trình."""

    node_id: str = Field(default="START")
    description: str = Field(default="Điểm bắt đầu của đơn vị chương trình")


class ProcessingBlock(CFGNode):
    """Khối xử lý chứa các câu lệnh khai báo hoặc tính toán."""

    description: str = Field(
        default="Khối xử lý chứa các câu lệnh khai báo hoặc tính toán"
    )
    statements: list[str] = Field(
        default_factory=list, description="Các câu lệnh khai báo hoặc tính toán"
    )

    def add_statement(self, statement: str) -> None:
        self.statements.append(statement)


class DecisionNode(CFGNode):
    """Điểm quyết định ứng với các câu lệnh điều kiện trong các khối lệnh rẽ nhánh hoặc lặp."""

    description: str = Field(default="Điểm quyết định (điều kiện rẽ nhánh/lặp)")
    condition: str = Field(..., description="Biểu thức điều kiện")
    true_node_id: str | None = Field(
        default=None, description="ID nút khi điều kiện Đúng"
    )
    false_node_id: str | None = Field(
        default=None, description="ID nút khi điều kiện Sai"
    )

    def set_branches(self, true_node: CFGNode, false_node: CFGNode) -> None:
        """Thiết lập hai nhánh Đúng / Sai."""
        self.true_node_id = true_node.node_id
        self.false_node_id = false_node.node_id
        self.next_node_ids = [true_node.node_id, false_node.node_id]


class JunctionNode(CFGNode):
    """Điểm nối ứng với các câu lệnh ngay sau các lệnh rẽ nhánh."""

    description: str = Field(default="Điểm nối ngay sau các lệnh rẽ nhánh")


class EndNode(CFGNode):
    """Điểm kết thúc ứng với điểm kết thúc của đơn vị chương trình."""

    node_id: str = Field(default="END")
    description: str = Field(default="Điểm kết thúc của đơn vị chương trình")


def foo(a: int, b: int, c: int, d: int):
    e: float
    if a == 0:
        return 0
    x: int = 0
    if a == b or c == d:
        x = 1
    e = 1 / x
    return e


def add_note():
    pass


def add_edge():
    pass


@llm_invoke
def build[**P, R](func: Callable[P, R], lang: str):
    src = inspect.getsource(func)
    return [
        HumanMessage(f"""Xây dựng đồ thị luồng điều khiển cho hàm sau:
```{lang}
{src}
```
""")
    ]


def main():
    result = build(foo, "python")
    print(result)


if __name__ == "__main__":
    main()

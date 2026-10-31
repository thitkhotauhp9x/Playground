import inspect

from langchain_core.messages import SystemMessage, HumanMessage

from app.libs.playground.utils.openai_runner import llm_invoke


def foo(a: int, b: int, c: int, d: int):
    e: float
    if a == 0:
        return 0
    x: int = 0
    if a == b or c == d:
        x = 1
    e = 1 / x
    return e


@llm_invoke
def do(source: str):
    return [
        SystemMessage("""Hướng dẫn đánh số các dòng lệnh của đơn vị chương trình theo step-by-step

Bước 1: Xác định điểm bắt đầu của chương trình.
- Là điểm khai báo chương trình, không được đánh số.
Bước 2: Xác định điểm kết thúc của chương trình.
- Là một điểm ảo nằm ngoài mã nguồn, không được đánh số.
- Được thực hiện sau câu lệnh return.
Bước 3: Đánh số các dòng lệnh của đơn vị chương trình (bắt đầu thừ 1) được thực hiện sau điểm bắt đầu và trước điểm kết thúc.
Bước 4: Đưa ra chương trình đã được đánh số các dòng lệnh.
"""),
        HumanMessage(f"""Đây là chương trình cần đánh số dòng lệnh:
```
{source}
```
"""),
    ]


@llm_invoke
def extract_result(result):
    return [
        HumanMessage(f"""Đưa ra chương trình đã được đánh số dòng lệnh mà không cần giải thích gì thêm.
<content>
{result}
<content>
""")
    ]


@llm_invoke
def do2(content):
    return [
        SystemMessage("""Xác định các đường đi tối thiểu (list[int]) đi qua các điểm để đảm bảo 100% độ phủ của độ đo \
C_1(Mỗi câu lệnh được thực\
 hiện ít nhất 1 lần sau khi chạy tất cả các ca kiểm thử.) theo từng bước sau.

Bước 1: Tạo mảng dữ liệu đánh dấu các điểm đi qua và điểm chưa đi qua.
Bước 1: Xác định đường đi dài nhất đi qua các điểm chưa đi qua.
Bước 2: Đánh dấu các điểm mà đường đi dài nhất trên đi qua thành điểm đã đi qua. Xác định các điểm chưa đi qua.
Bước 3: Nếu không còn điểm nào chưa đi qua thì thông báo các đường đi, Nếu còn điểm chưa đi qua quay lại bước 1

```
def find_longest_path(points: set[int], source: str) -> list[int]:
    #  Xác định đường đi dài nhất đi qua các điểm.
    pass

def do(points: set[int]):
    visited_points: set[int] = {}
    longest_path = find_longest_path(visited_points)
    for point in longest_path:
        visited_points += point
    
    pass
```"""),
        HumanMessage(content),
    ]


def main():
    source = inspect.getsource(foo)
    r1 = do(source)
    print(r1)

    r2 = extract_result(r1)
    print("***")
    print(r2)
    r3 = do2(r2)
    print("***")
    print(r3)


if __name__ == "__main__":
    main()

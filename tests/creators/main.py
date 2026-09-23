from typing import Iterable

from hat.decorators.air import air
from hat.playground.creators.instruction_creator import InstructionCreator


def main() -> None:
    response = InstructionCreator(
        prompt="Create instructions to solve a quadratic equation."
    ).create()

    @air
    def solve() -> Iterable[str]:
        yield f"""Use the following instructions to resolve the quadratic equation (x2 - 49x - 50 = 0)
{response}
"""

    response2 = solve()
    print(response2)

    response = InstructionCreator(
        prompt="""\
Create instructions to assert whether something is logically supported by an OpenAI response. \
The user provides a claim along with an OpenAI response. \
OpenAI will then evaluate whether the claim is true or false, and if it is false, provide the reason.\
"""
    ).create()
    print(response)


def main2():
    response = InstructionCreator(
        prompt="""
Cập nhật system_message để đảm bảo kết quả đầu ra ổn định. Bạn sẽ nhận được system_message, human_message và danh sách ai_messages (là các kết quả khi chạy cùng một human_message với system_message hiện tại). Hiện nay, các ai_messages này cho ra những kết quả khác nhau. Nhiệm vụ của bạn là phân tích sự khác biệt giữa các ai_messages, sau đó điều chỉnh lại system_message để cùng một human_message luôn tạo ra kết quả nhất quán.”
"""
    ).create()

    @air
    def solve() -> Iterable[str]:
        yield f"""Use the following instructions to resolve the quadratic equation (x2 - 49x - 50 = 0)
    {response}
    """

    print(response)


if __name__ == "__main__":
    main2()

import sys
import textwrap
from typing import Annotated

from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from playground.utils.openai_runner import chat_model

console = Console(force_terminal=True)


class Question(BaseModel):
    value: str
    example_answers: list[str]


class QuestionList(BaseModel):
    questions: Annotated[list[Question], Field(max_length=3)]


def query(response: str):
    output_parser = PydanticOutputParser(pydantic_object=QuestionList)
    question_list: QuestionList = output_parser.invoke(response)
    if not question_list.questions:
        return None
    content = ""
    for index, q in enumerate(question_list.questions):
        answer = Prompt.ask(q.value, choices=q.example_answers)
        content += f"""{index + 1}. {q.value}
<user_answer>
{textwrap.indent(answer, "  ", lambda line: True)}
</user_answer>
"""
    console.print(Markdown(content))
    return HumanMessage(content)


def step_1(work_description: str):
    output_parser = PydanticOutputParser(pydantic_object=QuestionList)

    content = f"""Bạn là một Kỹ sư Prompt xuất sắc (Expert Prompt Engineer). \
Nhiệm vụ của bạn là giúp tôi thiết kế một "Prompt Template" hoàn hảo nhất cho công việc dưới đây.

> {work_description}

Bây giờ, hãy thực hiện bước sau theo quy trình:

Bước 1: Đặt câu hỏi
* Nếu thông tin tôi cung cấp chưa đủ rõ ràng hoặc thiếu các yếu tố cốt lõi (như định dạng đầu ra, bối cảnh),
  hãy đặt cho tôi tối đa 3 câu hỏi để tôi làm rõ.
  {textwrap.indent(output_parser.get_format_instructions(), "  ", lambda line: True).strip()}
* Nếu đã đủ thông tin, hãy thông báo, "{QuestionList(questions=[]).model_dump_json(indent=2)}"
"""
    messages = [HumanMessage(content)]
    response = None
    for _ in range(10):
        try:
            response = chat_model.invoke(messages)
            messages.append(response)
            str_response = StrOutputParser().invoke(response)
            answer = query(str_response)
            if answer:
                messages.append(answer)
            else:
                print("Done step 1")
                step_2(messages)
        except Exception as err:
            print(err, file=sys.stderr)
            return response
    return response


def step_2(messages: list[BaseMessage]):
    inner_messages = [
        *messages,
        HumanMessage("""Bước 2: Đề xuất định dạng kết quả (Expected Output)
* Dựa trên công việc của tôi, hãy gợi ý 2-3 định dạng kết quả đầu ra chuyên nghiệp nhất (Ví dụ: Dạng bảng, \
dạng danh sách bullet-point, dạng bài viết có cấu trúc cụ thể...) để tôi có thể lựa chọn.
"""),
    ]
    response = chat_model.invoke(inner_messages)
    inner_messages.append(response)
    console.print(Markdown(StrOutputParser().invoke(response)))
    return inner_messages


def question(
    messages: list[BaseMessage],
    default: str = "Thông tin đã đủ, tiến hành tạo template.",
):
    output_parser = PydanticOutputParser(pydantic_object=QuestionList)
    #
    #     system_content = """Bạn là một Kỹ sư Prompt xuất sắc (Expert Prompt Engineer). \
    # Nhiệm vụ của bạn là giúp tôi thiết kế một "Prompt Template" hoàn hảo nhất cho công việc được người dùng nhập vào.
    #
    # Bây giờ, hãy thực hiện bước sau theo quy trình:
    # """
    #     step_1 = f"""Bước 1: Đặt câu hỏi
    # * Nếu thông tin tôi cung cấp chưa đủ rõ ràng hoặc thiếu các yếu tố cốt lõi (như định dạng đầu ra, bối cảnh), hãy đặt cho tôi tối đa 3 câu hỏi để tôi làm rõ.
    #   {textwrap.indent(output_parser.get_format_instructions(), "  ", lambda line: True).strip()}
    # * Nếu đã đủ thông tin, hãy thông báo, "{default}"
    # """
    #
    #     first_step = system_content + step_1
    #     _messages = [
    #         SystemMessage(first_step),
    #         HumanMessage(f"""This is the work:
    # > {work_description}
    # """)
    #     ]
    #     r1 = None
    #     for _ in range(10):
    #         try:
    #             r1 = chat_model.invoke(_messages)
    #             _messages.append(r1)
    #             _messages.append(query(StrOutputParser().invoke(r1)))
    #         except Exception as e:
    #             print(e)
    #             return r1
    #     return r1

    inner_messages = [
        SystemMessage(
            content=f"""Bạn là một Kỹ sư Prompt xuất sắc (Expert Prompt Engineer). \
Nhiệm vụ của bạn là giúp tôi thiết kế một "Prompt Template" hoàn hảo nhất cho công việc dưới đây.

1. Công việc tôi muốn làm: [Điền tên công việc, ví dụ: Viết bài review sản phẩm công nghệ]
2. Đối tượng mục tiêu đọc kết quả này: [Điền đối tượng, ví dụ: Người dùng phổ thông, học sinh, đối tác]
3. Yêu cầu đặc biệt (nếu có): [Điền yêu cầu, ví dụ: Giọng văn hài hước, ngắn gọn dưới 500 từ]

Bây giờ, hãy thực hiện các bước sau theo quy trình:

Bước 1: Đặt câu hỏi
* Nếu thông tin tôi cung cấp ở trên chưa đủ rõ ràng hoặc thiếu các yếu tố cốt\
 lõi (như định dạng đầu ra, bối cảnh), hãy đặt cho tôi tối đa 3 câu hỏi để tôi làm rõ.\
 Chú ý không hỏi lại những câu tôi đã trả lời.
 {textwrap.indent(output_parser.get_format_instructions(), "  ", lambda line: True).strip()}
* Nếu đã đủ thông tin, hãy thông báo, "{default}"

Bước 2: Đề xuất định dạng kết quả (Expected Output)
* Dựa trên công việc của tôi, hãy gợi ý 2-3 định dạng kết quả đầu ra chuyên nghiệp nhất (Ví dụ: Dạng bảng, \
dạng danh sách bullet-point, dạng bài viết có cấu trúc cụ thể...) để tôi có thể lựa chọn.

Bước 3: Tạo Prompt Template hoàn chỉnh
* Hãy thiết kế một Prompt Template tối ưu nhất, viết theo cấu trúc chuẩn dành cho AI (bao gồm: Vai trò, Bối cảnh, \
Nhiệm vụ cụ thể, Các ràng buộc/Quy tắc, và Khung thông tin đầu vào). Sử dụng các ký hiệu `[...]` cho những phần \
thông tin mà tôi cần tự điền vào sau này.
"""
        ),
        *messages,
    ]
    for _ in range(10):
        response = chat_model.invoke(inner_messages)
        inner_messages.append(response)
        try:
            str_response = StrOutputParser().invoke(response)
            inner_messages.append(query(str_response))
        except Exception as e:
            print(e)
            return response
    return None


def main():
    answer = step_1("draw a banana")
    print(answer)


if __name__ == "__main__":
    main()

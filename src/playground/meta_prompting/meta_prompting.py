from typing import Annotated, Literal

from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from playground.templates.function_output_parser import indent
from playground.utils.openai_runner import llm, chat_model


class FormInput(BaseModel):
    type: Literal["text"]
    placeholder: Annotated[str, Field(description="""Valid for text, search, url, tel, email, password, and number, the placeholder attribute provides a brief hint to the user as to what kind of information is expected in the field. It should be a word or short phrase that provides a hint as to the expected type of data, rather than an explanation or prompt. The text must not include carriage returns or line feeds. So for example if a field is expected to capture a user's first name, and its label is "First Name", a suitable placeholder might be "e.g., Mustafa".""")]


class FormField(BaseModel):
    label: Annotated[str, Field(description="The <label> HTML element represents a caption for an item in a user interface.")]
    input: Annotated[FormInput, Field(description="The <input> HTML element is used to create interactive controls for web-based forms in order to accept data from the user; a wide variety of types of input data and control widgets are available, depending on the device and user agent. The <input> element is one of the most powerful and complex in all of HTML due to the sheer number of combinations of input types and attributes.")]


class Form(BaseModel):
    fields: list[FormField]


def create_form(openai_response: str) -> Form:
    output_parser = PydanticOutputParser(pydantic_object=Form)
    _llm = chat_model | output_parser

    return _llm.invoke([
        SystemMessage(f"""You are a form designer.
Nhiệm vụ của bạn là xác định xem phản hồi từ OpenAI cần thu thập dữ liệu nào từ người dùng hay không.
* Nếu cần thu thập yêu cầu từ người dùng thì thiết kế một biểu mẫu để làm việc trên.
  {indent(output_parser.get_format_instructions(), "  ")}
* Nếu không cần thu thuật dữ liệu nào từ người dùng thì trả về null form với nội dung như sau {Form(fields=[]).model_dump_json(indent=2)}
"""),
        HumanMessage(f"""This is a OpenAI response:
<openai_response>
{openai_response}
</openai_response>
""")
])


def step_1(messages: list[BaseMessage]) -> Form | None:
    class Response(BaseModel):
        reason: str
        questions: Annotated[list[str] | None, Field(description="Nếu đã đủ thông tin giá trị bàng null. Nếu thiếu thì đưa ra danh sách các câu hỏi để làm rõ thông tin.")] = None

    response: Response = Response(reason="")
    if response.questions:
        return create_form(str(response.questions))
    return None


def create_prompt_template(messages: list[BaseMessage]) -> str:
    return llm.invoke([
        SystemMessage("""Bạn là một Kỹ sư Prompt xuất sắc (Expert Prompt Engineer). \
Nhiệm vụ của bạn là giúp tôi thiết kế một "Prompt Template" hoàn hảo nhất cho công việc dưới đây.
"""),
        *messages,
    ])


def prompt():
    messages = [SystemMessage("""Bạn là một Kỹ sư Prompt xuất sắc (Expert Prompt Engineer). \
Nhiệm vụ của bạn là giúp tôi thiết kế một "Prompt Template" hoàn hảo nhất cho công việc dưới đây.

1. Công việc tôi muốn làm: [Điền tên công việc, ví dụ: Viết bài review sản phẩm công nghệ]
2. Đối tượng mục tiêu đọc kết quả này: [Điền đối tượng, ví dụ: Người dùng phổ thông, học sinh, đối tác]
3. Yêu cầu đặc biệt (nếu có): [Điền yêu cầu, ví dụ: Giọng văn hài hước, ngắn gọn dưới 500 từ]

Bây giờ, hãy thực hiện các bước sau theo quy trình:

Bước 1: Đặt câu hỏi (Nếu cần)
Nếu thông tin tôi cung cấp ở trên chưa đủ rõ ràng hoặc thiếu các yếu tố cốt lõi (như định dạng đầu ra, bối cảnh), \
hãy đặt cho tôi tối đa 3 câu hỏi trắc nghiệm hoặc ngắn gọn để tôi làm rõ. \
Nếu đã đủ thông tin, hãy bỏ qua bước này và thông báo "Thông tin đã đủ, tiến hành tạo template".

Bước 2: Đề xuất định dạng kết quả (Expected Output)
Dựa trên công việc của tôi, hãy gợi ý 2-3 định dạng kết quả đầu ra chuyên nghiệp nhất (Ví dụ: Dạng bảng, \
dạng danh sách bullet-point, dạng bài viết có cấu trúc cụ thể...) để tôi có thể lựa chọn.

Bước 3: Tạo Prompt Template hoàn chỉnh
Hãy thiết kế một Prompt Template tối ưu nhất, viết theo cấu trúc chuẩn dành cho AI (bao gồm: Vai trò, Bối cảnh, \
Nhiệm vụ cụ thể, Các ràng buộc/Quy tắc, và Khung thông tin đầu vào). Sử dụng các ký hiệu `[...]` cho những phần \
thông tin mà tôi cần tự điền vào sau này.
""")]
    # response = llm.invoke([SystemMessage(design_prompt_template())])
    # print(response)


def main() -> None:
    messages: list[BaseMessage] = [HumanMessage(content="Draw a banana.")]
    for _ in range(3):
        response = create_prompt_template(messages)
        form = create_form(response)
        if form:
            print(form.model_dump_json(indent=2))
            human_message: HumanMessage = ...
            messages.append(human_message)
        # return response


if __name__ == "__main__":
    main()

from langchain_core.messages import HumanMessage

from app.libs.playground.utils.openai_runner import llm_invoke


@llm_invoke
def mermaid(word: str):
    return [
        HumanMessage(f"""Hãy vẽ sơ đồ State Machine (sơ đồ chuyển đổi trạng thái) bằng Mermaid Diagram thể hiện quy trình chuyển đổi từ loại của gốc từ "{word}". 

Để tránh lỗi cú pháp (Lexical/Parsing error) của Mermaid, bạn hãy tuân thủ nghiêm ngặt các quy tắc sau:
1. Sử dụng cú pháp `stateDiagram-v2`.
2. KHÔNG sử dụng câu lệnh `note` độc lập bên ngoài (ví dụ: không dùng "note right of", "note Ready of").
3. Viết thông tin của trạng thái trực tiếp vào nhãn (label) bằng cú pháp: state "Tên trạng thái\n• Thông tin chi tiết 1\n• Thông tin chi tiết 2" as Mã_Trạng_Thái.
4. Mỗi trạng thái cần hiển thị rõ ràng: Từ loại (Part of speech), Từ tiếng Anh (English word), và Nghĩa tiếng Việt (Vietnamese meaning).
5. Các mũi tên chuyển đổi trạng thái (-->) chỉ ghi nhãn ngắn gọn về cách chuyển đổi từ (ví dụ: Thêm hậu tố, Giữ nguyên từ).
6. Sử dụng thẻ <br> để xuống dòng.

Sau sơ đồ, hãy giải thích song ngữ (Anh - Việt) ý nghĩa của trạng thái trước và sau khi chuyển đổi.
""")
    ]

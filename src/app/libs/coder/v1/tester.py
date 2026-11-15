from typing import Literal

import dspy


class Tester(dspy.Signature):
    """Đánh giá lời giải của coder dựa trên yêu cầu gốc."""

    task: str = dspy.InputField(desc="Yêu cầu gốc")
    code_output: str = dspy.InputField(desc="Code hoặc lời giải từ coder")

    errors: list[str] = dspy.OutputField(desc="Các lỗi hoặc rủi ro")
    edge_cases: list[str] = dspy.OutputField(desc="Các edge case cần xem xét")
    suggestions: list[str] = dspy.OutputField(desc="Đề xuất sửa cụ thể cho coder")
    verdict: Literal["PASS", "NEEDS_FIX"] = dspy.OutputField(
        desc="PASS nếu không có lỗi nghiêm trọng; nếu không, NEEDS_FIX"
    )

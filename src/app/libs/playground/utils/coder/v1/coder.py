import dspy


class Coder(dspy.Signature):
    """Viết code theo yêu cầu người dùng và phản hồi từ tester."""

    task: str = dspy.InputField(desc="Yêu cầu cần thực hiện")
    tester_feedback: str = dspy.InputField(desc="Phản hồi từ tester")

    analysis: str = dspy.OutputField(desc="Phân tích ngắn")
    code: str = dspy.OutputField(desc="Code hoàn chỉnh")
    explanation: str = dspy.OutputField(desc="Giải thích ngắn")

import dspy


class RefinedRAGSignature(dspy.Signature):
    """Trả lời câu hỏi dựa trên ngữ cảnh và góp ý cải thiện (nếu có từ lần thử trước)."""

    context: list[str] = dspy.InputField(desc="Ngữ cảnh truy xuất từ DB")
    question: str = dspy.InputField(desc="Câu hỏi của người dùng")
    feedback: str = dspy.InputField(
        desc="Lý do/góp ý khiến câu trả lời trước chưa đạt điểm cao (nếu có)"
    )
    answer: str = dspy.OutputField(desc="Câu trả lời hoàn chỉnh đã được cải thiện")

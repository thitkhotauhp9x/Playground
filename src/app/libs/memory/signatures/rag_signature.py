import dspy


class RAGSignature(dspy.Signature):
    """Trả lời câu hỏi một cách chính xác dựa trên các ngữ cảnh được truy xuất."""

    context: list[str] = dspy.InputField(desc="Danh sách các đoạn văn ngữ cảnh truy xuất từ DB")
    question: str = dspy.InputField(desc="Câu hỏi của người dùng")
    answer: str = dspy.OutputField(desc="Câu trả lời hoàn chỉnh và chính xác dựa trên ngữ cảnh")

import dspy


class JudgeSignature(dspy.Signature):
    """Đánh giá chất lượng câu trả lời của hệ thống theo thang điểm từ 1.0 đến 10.0."""

    question: str = dspy.InputField(desc="Câu hỏi ban đầu")
    reference_answer: str = dspy.InputField(desc="Đáp án chuẩn hoặc tiêu chí tham chiếu")
    user_answer: str = dspy.InputField(desc="Câu trả lời do hệ thống RAG sinh ra")

    reasoning: str = dspy.OutputField(desc="Phân tích ưu điểm, nhược điểm và lý do cho điểm")
    score: float = dspy.OutputField(desc="Điểm số đánh giá từ 1.0 đến 10.0")

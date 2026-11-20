import dspy

from app.libs.memory.db import retrieve_context_from_db, save_evaluation_to_db
from app.libs.memory.signatures.judge_signature import JudgeSignature
from app.libs.memory.signatures.refined_rag_signature import RefinedRAGSignature


# 2. Cấu trúc Pipeline với cơ chế Retry
class AutoRetryRAGPipeline(dspy.Module):
    def __init__(self, threshold: float = 7.0, max_retries: int = 3):
        super().__init__()
        self.threshold = threshold  # Ngưỡng điểm tối thiểu (VD: 7.0)
        self.max_retries = max_retries  # Số lần thử lại tối đa
        self.rag_generator = dspy.ChainOfThought(RefinedRAGSignature)
        self.evaluator = dspy.ChainOfThought(JudgeSignature)

    def forward(self, question: str, reference_answer: str = ""):
        context = retrieve_context_from_db(question)

        feedback = "Chưa có góp ý (Lần thử đầu tiên)."
        best_result = {}

        for attempt in range(1, self.max_retries + 1):
            print(f"🔄 [Lần thử {attempt}/{self.max_retries}] Đang sinh câu trả lời...")

            # A. Sinh câu trả lời (có kèm feedback nếu là lần retry)
            rag_res = self.rag_generator(context=context, question=question, feedback=feedback)
            current_answer = rag_res.answer

            # B. Đánh giá chất lượng
            ref = reference_answer or "Trả lời đầy đủ, chính xác và bám sát ngữ cảnh."
            eval_res = self.evaluator(
                question=question, reference_answer=ref, user_answer=current_answer
            )

            try:
                score_val = float(eval_res.score)
            except (ValueError, TypeError):
                score_val = 5.0

            print(f"   📊 Điểm số: {score_val}/10 | Lý do: {eval_res.reasoning[:80]}...")

            # Lưu thông tin kết quả
            best_result = {
                "attempts": attempt,
                "answer": current_answer,
                "reasoning": eval_res.reasoning,
                "score": score_val,
            }

            # C. Kiểm tra điều kiện đạt ngưỡng
            if score_val >= self.threshold:
                print(f"✅ Đạt yêu cầu chất lượng (>= {self.threshold})!")
                break
            print(f"⚠️ Điểm quá thấp (< {self.threshold}). Đang chuẩn bị thử lại...")
            # Cập nhật feedback để LLM rút kinh nghiệm ở lượt tiếp theo
            feedback = (
                f"Lần trả lời trước chỉ đạt {score_val}/10."
                f"Lý do kém: {eval_res.reasoning}."
                f"Hãy khắc phục các nhược điểm này."
            )

        # D. Lưu kết quả cuối cùng vào DB
        save_evaluation_to_db(
            question=question,
            answer=best_result["answer"],
            reasoning=best_result["reasoning"],
            score=best_result["score"],
        )

        return best_result

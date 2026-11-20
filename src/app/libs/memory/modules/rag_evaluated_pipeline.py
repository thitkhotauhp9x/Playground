import dspy

from app.libs.memory import JudgeSignature, retrieve_context_from_db, save_evaluation_to_db
from app.libs.memory.signatures.rag_signature import RAGSignature


class RAGEvaluatedPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        # Sử dụng ChainOfThought để tự động suy luận từng bước
        self.rag_generator = dspy.ChainOfThought(RAGSignature)
        self.evaluator = dspy.ChainOfThought(JudgeSignature)

    def forward(self, question: str, reference_answer: str = ""):
        # 1. Truy xuất dữ liệu từ DB (Retrieval)
        context = retrieve_context_from_db(question)

        # 2. Sinh câu trả lời (RAG Generation)
        rag_res = self.rag_generator(context=context, question=question)
        generated_answer = rag_res.answer

        # 3. Đánh giá câu trả lời (Evaluation)
        ref = reference_answer or "Trả lời đầy đủ, chính xác và bám sát ngữ cảnh."
        eval_res = self.evaluator(
            question=question, reference_answer=ref, user_answer=generated_answer
        )

        # Xử lý điểm số an toàn
        try:
            score_val = float(eval_res.score)
        except (ValueError, TypeError):
            score_val = 5.0

        # 4. Lưu vết vào Cơ sở dữ liệu
        save_evaluation_to_db(
            question=question,
            answer=generated_answer,
            reasoning=eval_res.reasoning,
            score=score_val,
        )

        return {
            "question": question,
            "context": context,
            "answer": generated_answer,
            "reasoning": eval_res.reasoning,
            "score": score_val,
        }

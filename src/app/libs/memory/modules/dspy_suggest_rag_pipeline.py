import dspy

from app.libs.memory import JudgeSignature, retrieve_context_from_db, save_evaluation_to_db
from app.libs.memory.signatures.rag_signature import RAGSignature


class DSPySuggestRAGPipeline(dspy.Module):
    def __init__(self, threshold: float = 7.0):
        super().__init__()
        self.threshold = threshold
        self.rag_generator = dspy.ChainOfThought(RAGSignature)
        self.evaluator = dspy.ChainOfThought(JudgeSignature)

    def forward(self, question: str, reference_answer: str = ""):
        context = retrieve_context_from_db(question)
        rag_res = self.rag_generator(context=context, question=question)

        ref = reference_answer or "Trả lời đầy đủ, chính xác và bám sát ngữ cảnh."
        eval_res = self.evaluator(
            question=question, reference_answer=ref, user_answer=rag_res.answer
        )
        score_val = float(eval_res.score)

        # Kích hoạt Backtrack nếu điểm số chưa đạt yêu cầu
        dspy.Suggest(
            score_val >= self.threshold,
            msg=f"Câu trả lời chưa đạt (điểm số: {score_val}/10.0 < {self.threshold}). "
            f"Nhận xét: {eval_res.reasoning}. Hãy cải thiện để trả lời chính xác hơn.",
        )

        save_evaluation_to_db(question, rag_res.answer, eval_res.reasoning, score_val)

        return {
            "question": question,
            "context": context,
            "answer": rag_res.answer,
            "reasoning": eval_res.reasoning,
            "score": score_val,
        }

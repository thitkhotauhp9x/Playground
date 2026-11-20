import math
from collections.abc import Callable, Iterable

import dspy

from app.libs.generated_knowledge_prompting.checker import hcs, moe, poe
from app.libs.generated_knowledge_prompting.knowledge_integration import KnowledgeIntegration


def softmax[T](items: Iterable[T], key: Callable[[T], float]) -> list[tuple[T, float]]:
    return [(item, 100 * math.exp(key(item))) for item in items]


class KnowledgeIntegrator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(KnowledgeIntegration)
        lm = dspy.LM("openai/gpt-4o-mini", logprobs=True)
        self.predict.set_lm(lm)

    def forward(self, question, knowledge_list, choices):
        predictions = []
        probs = []
        answers = []
        lm = self.predict.lm
        for knowledge in knowledge_list:
            result = self.predict(question=question, knowledge=knowledge, choices=choices)
            if lm and lm.history:
                history = lm.history[-1]
                tokens = history["outputs"][0]["logprobs"]["content"]
                answer_tokens = [*tokens]

                total_logprob = sum(token["logprob"] for token in answer_tokens)
                probs.append(total_logprob)
                answers.append(result.answer)
                predictions.append((result.answer, total_logprob))
        result = softmax(predictions, key=lambda x: x[1])
        print("hcs", hcs(answers, probs))
        print("moe", moe(answers, probs))
        print("moe", poe(answers, probs))
        return result

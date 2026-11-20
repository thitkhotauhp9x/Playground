import dspy

from app.libs.generated_knowledge_prompting.knowledge_generation import KnowledgeGeneration


class KnowledgeGenerator(dspy.Module):
    def __init__(self, num_knowledge=20):
        super().__init__()
        self.num_knowledge = num_knowledge
        self.generate = dspy.Predict(KnowledgeGeneration)

    def forward(self, question: str) -> list[str]:
        result = self.generate(question=question)

        # Remove empty and duplicate knowledge
        knowledge = list(
            dict.fromkeys(k.strip() for k in result.generated_knowledge if k and k.strip())
        )

        return knowledge[: self.num_knowledge]

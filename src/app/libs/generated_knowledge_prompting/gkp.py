import dspy

from app.libs.generated_knowledge_prompting.knowledge_generator import KnowledgeGenerator
from app.libs.generated_knowledge_prompting.knowledge_integrator import KnowledgeIntegrator


class GKP(dspy.Module):
    def __init__(self, num_knowledge=20):
        super().__init__()

        self.knowledge_generator = KnowledgeGenerator(num_knowledge=num_knowledge)

        self.knowledge_integrator = KnowledgeIntegrator()

    def forward(self, question: str, choices: list[str]):
        knowledge_list = self.knowledge_generator(question=question)

        integration_result = self.knowledge_integrator(
            question=question, knowledge_list=knowledge_list, choices=choices
        )
        print(knowledge_list)
        print(integration_result)

        result = max(integration_result, key=lambda x: x[1])
        return result[0][0], result[1]

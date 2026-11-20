import dspy


class KnowledgeGeneration(dspy.Signature):
    """
    Generate relevant commonsense knowledge that can help answer
    the given question.

    The generated knowledge should provide useful factual information
    rather than directly answering the question.
    """

    question: str = dspy.InputField(desc="The question that requires commonsense reasoning.")

    generated_knowledge: list[str] = dspy.OutputField(
        desc=(
            "A list of distinct, relevant factual knowledge statements "
            "that can help answer the question. Each item should express "
            "one useful piece of knowledge."
        )
    )

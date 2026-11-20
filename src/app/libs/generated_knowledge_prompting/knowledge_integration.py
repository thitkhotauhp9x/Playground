import dspy


class KnowledgeIntegration(dspy.Signature):
    """
    Answer a question using additional generated knowledge.

    Use the provided knowledge as supporting context.
    Select the most appropriate answer from the candidates.
    """

    question: str = dspy.InputField(desc="The original question.")

    knowledge: str = dspy.InputField(
        desc="A generated knowledge statement relevant to the question."
    )

    choices: list[str] = dspy.InputField(desc="The candidate answers.")

    answer: str = dspy.OutputField(
        desc="The selected answer. Must match one of the candidate answers."
    )

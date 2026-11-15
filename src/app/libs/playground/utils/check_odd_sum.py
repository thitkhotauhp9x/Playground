import dspy
from dspy import Evaluate

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))


class CheckOddSum(dspy.Signature):
    """Determine whether the odd numbers in the group sum to an even number."""

    question: str = dspy.InputField()
    answer: bool = dspy.OutputField()


cot = dspy.ChainOfThought(CheckOddSum)

train_set = [
    dspy.Example(
        question="The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.",
        answer=False,
    ).with_inputs("question"),
    dspy.Example(
        question="The odd numbers in this group add up to an"
        " even number: 17, 10, 19, 4, 8, 12, 24.",
        answer=True,
    ).with_inputs("question"),
    dspy.Example(
        question="The odd numbers in this group add up"
        " to an even number: 16, 11, 14, 4, 8, 13, 24.",
        answer=True,
    ).with_inputs("question"),
    dspy.Example(
        question="The odd numbers in this group add up to an even number: 17, 9, 10, 12, 13, 4, 2.",
        answer=False,
    ).with_inputs("question"),
]


def exact_match(example, pred, trace=None):
    return example.answer == pred.answer


def evaluate():
    evaluator = Evaluate(
        devset=train_set,
        metric=exact_match,
        num_threads=1,
        display_progress=True,
        display_table=4,
    )

    evaluator(cot)

    for example in train_set:
        pred = cot(**example.inputs())
        print("Question:", example.question)
        print("Reasoning:", pred.reasoning)
        print("Answer:", pred.answer)


if __name__ == "__main__":
    evaluate()

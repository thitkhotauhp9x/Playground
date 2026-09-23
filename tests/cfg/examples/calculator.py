import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)


class Calculator(dspy.Signature):
    """
    result = a^2 - b^2
    """

    a: int = dspy.InputField()
    b: int = dspy.InputField()
    result: int = dspy.OutputField()


def main():
    model = dspy.ChainOfThought(Calculator)
    response = model(a=1, b=2)
    assert response.result == -3


if __name__ == "__main__":
    main()

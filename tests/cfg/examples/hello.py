import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)


class Hello(dspy.Signature):
    """
    result = f"Hello {name}"
    """

    name: str = dspy.InputField()
    result: str = dspy.OutputField()


def main():
    model = dspy.ChainOfThought(Hello)
    response = model(name="John")
    print(response)
    assert response.result == "Hello John"


if __name__ == "__main__":
    main()

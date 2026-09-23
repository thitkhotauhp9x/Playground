import dspy

dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))
dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)


def test_assign_emtpy_string() -> None:
    class Model(dspy.Signature):
        """
        result = an empty string
        result = var if var
        """
        var: str | None = dspy.InputField()
        result: str = dspy.OutputField()

    model = dspy.ChainOfThought(Model)
    response = model(var="None")
    assert response.result == ""


def test_join_string() -> None:
    class Model(dspy.Signature):
        """
        result = an empty string
        result = var-{var}-{var}-var if var
        """
        var: str | None = dspy.InputField()
        result: str = dspy.OutputField()

    model = dspy.ChainOfThought(Model)
    response = model(var="Jame")
    assert response.result == 'var-Jame-Jame-var'

def test_assign_string() -> None:
    class Model(dspy.Signature):
        """
        Execute the following instructions step-by-step. Do not skip any instructions.
        result = "None"
        result = "{var}"
        result = "{var}-var"
        result = "None"
        """
        var: str = dspy.InputField()
        result: str = dspy.OutputField(desc="The final value of `result`")

    model = dspy.ChainOfThought(Model)
    response = model(var="")
    # print(dspy.inspect_history())
    assert response.result == "None"


def test_condition() -> None:
    class Model(dspy.Signature):
        """
        Execute the following instructions step-by-step. Do not skip any instructions.
        result = "xxx" if "{var}" == "" else "{var}"
        """
        var: str = dspy.InputField()
        result: str = dspy.OutputField(desc="The final value of `result`")

    model = dspy.ChainOfThought(Model)
    response = model(var="")
    print(dspy.inspect_history())
    assert response.result == "xxx"


def test_question() -> None:
    class Model(dspy.Signature):
        """Execute each step exactly as specified, in the given order, without skipping, reordering, or combining any steps.
        Complete each step before proceeding to the next.
        For each step, explicitly specify:
        - Input: the data or state before executing the step.
        - Output: the data or state immediately after executing the step.

        This is steps:
        Step 1: result = What is the capital of Vietnam?
        Step 2: result = "The capital of Vietnam is {result}"
        """
        var: str = dspy.InputField()
        result: str = dspy.OutputField(desc="The final value of `result`")

    model = dspy.ChainOfThought(Model)
    response = model(var="...")
    print(dspy.inspect_history())
    assert response.result == "The capital of Vietnam is Hanoi."

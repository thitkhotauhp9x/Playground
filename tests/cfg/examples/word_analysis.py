import dspy

dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))
dspy.configure_cache(enable_disk_cache=False, enable_memory_cache=False)


class WordAnalysis(dspy.Signature):
    """
    Extract the prefix of the given word. If no prefix is found, return an empty string (""). Do not add any extra text, explanations, or quotes.
    Extract the suffix of the given word. If no suffix is found, return an empty string (""). Do not add any extra text, explanations, or quotes.
    """
    word: str = dspy.InputField()
    prefix: str = dspy.OutputField()
    root: str = dspy.OutputField()
    suffix: str = dspy.OutputField()


def main():
    model = dspy.ChainOfThought(WordAnalysis)
    word = "hopeless"

    for _ in range(0, 6):
        response = model(word=word)
        print(response)

        if response.prefix or response.suffix:
            word = response.root
        else:
            break


if __name__ == '__main__':
    main()

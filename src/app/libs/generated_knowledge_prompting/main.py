import dspy

from app.libs.generated_knowledge_prompting.gkp import GKP

lm = dspy.LM("openai/gpt-5.4", logprobs=True)
dspy.configure(lm=lm)


def main():
    question = "Tôi sinh năm 2023 thì năm 2180 tôi đang sống hay đã chết?"

    choices = [
        "Sống",
        "Chết",
        "Không biết",
    ]
    gkp = GKP()

    result = gkp(question=question, choices=choices)

    print("=== Generated Knowledge ===")
    print(result)


if __name__ == "__main__":
    main()

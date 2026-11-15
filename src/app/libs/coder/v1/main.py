import dspy
from rich.console import Console
from rich.markdown import Markdown

from app.libs.coder.v1.coder import Coder
from app.libs.coder.v1.markdown_converters import MarkdownConverter
from app.libs.coder.v1.tester import Tester

dspy.configure(lm=dspy.LM("openai/gpt-5-mini"))


console = Console(force_terminal=True)


def run_collaboration(task: str, rounds: int = 2):
    coder = dspy.ChainOfThought(Coder)
    tester = dspy.ChainOfThought(Tester)

    converter = MarkdownConverter()

    tester_result = ""
    coder_result = coder(task=task, tester_feedback=tester_result)
    import pdb

    pdb.set_trace()
    console.print(Markdown(converter.coder_result_to_markdown(coder_result)))

    for i in range(rounds):
        tester_result = tester(task=task, code_output=coder_result.code)
        console.print(Markdown(converter.tester_result_to_markdown(tester_result)))

        if tester_result.verdict == "PASS":
            break
        coder_result = coder(
            task=task, tester_feedback=converter.coder_result_to_markdown(coder_result)
        )
        console.print(Markdown(converter.coder_result_to_markdown(coder_result)))

    return {"final_result": coder_result, "tester_review": tester_result}


if __name__ == "__main__":
    task = (
        "Viết hàm Python kiểm tra chuỗi palindrome,"
        " bỏ qua khoảng trắng và không phân biệt hoa thường."
    )
    result = run_collaboration(task, rounds=3)

    converter = MarkdownConverter()
    console.print("=== FINAL RESULT ===")
    console.print(Markdown(converter.coder_result_to_markdown(result["final_result"])))

    console.print("\n=== TESTER REVIEW ===")
    console.print(Markdown(converter.tester_result_to_markdown(result["tester_review"])))

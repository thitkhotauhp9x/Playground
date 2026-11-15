from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

console = Console(force_terminal=True)
client = OpenAI()


def coder_agent(task: str, tester_feedback: str = "") -> str:
    prompt = f"""
Bạn là CODER.
Nhiệm vụ: viết code theo yêu cầu người dùng.

Yêu cầu:
{task}

Phản hồi từ tester:
{tester_feedback}

Hãy trả về:
1. Phân tích ngắn
2. Code hoàn chỉnh
3. Giải thích ngắn
"""
    response = client.responses.create(model="gpt-5.4", input=prompt)
    console.print(Markdown("# Coder implement"))
    console.print(Markdown(response.output_text))
    return response.output_text


def tester_agent(task: str, code_output: str) -> str:
    prompt = f"""
Bạn là TESTER.
Nhiệm vụ: tìm bug, edge case, lỗi logic trong lời giải của coder.

Yêu cầu gốc:
{task}

Code/lời giải từ coder:
{code_output}

Hãy trả về:
1. Các lỗi hoặc rủi ro
2. Edge cases
3. Đề xuất sửa rõ ràng cho coder
Nếu không có lỗi nghiêm trọng, hãy nói 'PASS'.
"""
    response = client.responses.create(model="gpt-5.4", input=prompt)
    console.print(Markdown("# Tester review"))
    console.print(Markdown(response.output_text))
    return response.output_text


def run_collaboration(task: str, rounds: int = 2):
    coder_result = coder_agent(task)

    for i in range(rounds):
        tester_result = tester_agent(task, coder_result)

        if "PASS" in tester_result.upper():
            break
        coder_result = coder_agent(task, tester_result)

    return {"final_result": coder_result, "tester_review": tester_result}


if __name__ == "__main__":
    task = (
        "Viết hàm Python kiểm tra chuỗi palindrome,"
        " bỏ qua khoảng trắng và không phân biệt hoa thường."
    )
    result = run_collaboration(task, rounds=3)

    console.print("=== FINAL RESULT ===")
    console.print(Markdown(result["final_result"]))
    console.print("\n=== TESTER REVIEW ===")
    console.print(Markdown(result["tester_review"]))

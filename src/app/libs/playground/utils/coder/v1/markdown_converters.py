from dspy import Prediction


class MarkdownConverter:
    @staticmethod
    def coder_result_to_markdown(coder: Prediction):
        return f"""# Coder result
Phân tích ngắn:
{coder.analysis}

Code hoàn chỉnh:
{coder.code}

Giải thích ngắn:
{coder.explanation}
"""

    @staticmethod
    def tester_result_to_markdown(tester: Prediction):
        return f"""# Tester result

Các lỗi hoặc rủi ro:
{tester.errors}

Các edge case cần xem xét:
{tester.edge_cases}

Đề xuất sửa cụ thể cho coder:
{tester.suggestions}

Kết luận:
{tester.verdict}
"""

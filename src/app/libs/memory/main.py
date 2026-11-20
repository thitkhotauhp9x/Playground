import os

import dspy

from app.libs.memory.db import init_db
from app.libs.memory.modules.auto_retry_rag_pipeline import AutoRetryRAGPipeline

if __name__ == "__main__":
    print("🚀 Đang khởi tạo ứng dụng DSPy RAG + Evaluation + Database...")
    init_db()

    # Cấu hình Language Model (LM)
    # Lưu ý: Cần gán OPENAI_API_KEY trong môi trường hệ thống
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️ CẢNH BÁO: Chưa tìm thấy OPENAI_API_KEY trong môi trường.")
        print("Vui lòng thiết lập biến môi trường trước khi chạy, ví dụ:")
        print("export OPENAI_API_KEY='your-api-key-here'\n")
        # Giả lập để minh họa mã nguồn nếu không có API key
        dspy.configure(
            lm=dspy.LM("openai/gpt-4o-mini", api_key="sk-dummy-key-for-script-validation")
        )
    else:
        lm = dspy.LM("openai/gpt-4o-mini")
        dspy.configure(lm=lm)

    # Khởi tạo Pipeline
    pipeline = AutoRetryRAGPipeline()

    test_question = """Nếu tôi sinh ra vào ngày hôm nay thì năm 2200 tôi đang sống hay đã chết?
    (A còn sống, B đã chết, C không biết) chỉ được phép lựa chọn một đáp án.
    """
    print(f"\n❓ [CÂU HỎI]: {test_question}")

    result = pipeline(question=test_question, reference_answer=None)

    print(result)

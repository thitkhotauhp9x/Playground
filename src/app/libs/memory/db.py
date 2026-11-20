import sqlite3

DB_NAME = "dspy_rag_app.db"


def init_db():
    """Tạo các bảng dữ liệu nếu chưa tồn tại và nạp dữ liệu mẫu vào Knowledge Base."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Bảng 1: Lưu kiến thức dùng cho RAG (Knowledge Base)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    """)

    # Bảng 2: Lưu kết quả đánh giá (Evaluations)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            reasoning TEXT,
            score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Nạp dữ liệu mẫu vào Knowledge Base nếu bảng còn trống
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    if cursor.fetchone()[0] == 0:
        sample_docs = [
            (
                "Khái niệm DSPy",
                "DSPy (Declarative Self-improving Python) là một framework"
                " do Đại học Stanford phát triển giúp lập trình hóa các"
                " lời gọi LLM thay vì viết prompt thủ công.",
            ),
            (
                "RAG trong DSPy",
                "Trong DSPy, RAG được triển khai bằng cách kết hợp dspy."
                "Retrieve hoặc custom retriever với Signature để truyền context vào LLM.",
            ),
            (
                "LLM-as-a-Judge",
                "Phương pháp LLM-as-a-Judge sử dụng một mô hình LLM để tự"
                " động đánh giá chất lượng câu trả lời của một mô hình khác"
                " dựa trên các tiêu chí cụ thể.",
            ),
        ]
        cursor.executemany("INSERT INTO knowledge_base (title, content) VALUES (?, ?)", sample_docs)
        print("✅ Đã nạp dữ liệu mẫu vào Knowledge Base.")

    conn.commit()
    conn.close()


def retrieve_context_from_db(query: str, limit: int = 2) -> list[str]:
    """Hàm tìm kiếm ngữ cảnh đơn giản từ cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tìm kiếm các bài viết chứa từ khóa hoặc lấy tất cả nếu không khớp từ khóa
    words = query.split()
    conditions = " OR ".join(["content LIKE ?" for _ in words])
    params = [f"%{word}%" for word in words]

    sql = f"SELECT title, content FROM knowledge_base WHERE {conditions} LIMIT {limit}"
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    if not rows:
        cursor.execute("SELECT title, content FROM knowledge_base LIMIT ?", (limit,))
        rows = cursor.fetchall()

    conn.close()
    return [f"[{row[0]}]: {row[1]}" for row in rows]


def save_evaluation_to_db(question: str, answer: str, reasoning: str, score: float):
    """Lưu kết quả đánh giá vào SQLite DB."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO evaluations (question, answer, reasoning, score) VALUES (?, ?, ?, ?)",
        (question, answer, reasoning, score),
    )
    conn.commit()
    conn.close()
    print("💾 Đã lưu lượt đánh giá vào cơ sở dữ liệu (SQLite).")


def get_all_evaluations():
    """Đọc toàn bộ lịch sử đánh giá trong DB."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question, answer, score, created_at FROM evaluations ORDER BY id DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

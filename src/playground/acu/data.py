import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

# --- CẤU HÌNH ---
PDF_PATH = "tai_lieu_cua_ban.pdf"  # Thay bằng đường dẫn file PDF của bạn
MODEL_EMBEDDING = "nomic-embed-text"


def main():
    # 1. Đọc dữ liệu từ file PDF
    if not os.path.exists(PDF_PATH):
        print(f"❌ Không tìm thấy file PDF tại: {PDF_PATH}")
        return

    print("📖 Đang đọc file PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"✅ Đã đọc xong. Tổng số trang: {len(documents)}")

    # 2. Chia nhỏ văn bản (Chunking) để embedding chính xác hơn
    print("✂️ Đang cắt nhỏ văn bản...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Độ dài mỗi đoạn (ký tự)
        chunk_overlap=200  # Phần trùng lặp giữa các đoạn để không mất ngữ cảnh
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Đã chia thành {len(chunks)} đoạn văn nhỏ.")

    # 3. Khởi tạo mô hình Embedding từ Ollama
    print(f"🤖 Đang kết nối với Ollama để lấy mô hình: {MODEL_EMBEDDING}...")
    embeddings = OllamaEmbeddings(model=MODEL_EMBEDDING)

    # 4. Tạo Vector Database và lưu vào bộ nhớ (In-Memory)
    # Lưu ý: Nếu muốn lưu thành file trên ổ cứng để dùng lại, thêm tham số: persist_directory="./chroma_db"
    print("🧠 Đang tiến hành tạo vector dữ liệu và nạp vào ChromaDB...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    print("✅ Hệ thống đã sẵn sàng tìm kiếm!\n" + "=" * 40)

    # 5. Thử nghiệm tìm kiếm ngữ nghĩa (Semantic Search)
    while True:
        query = input("\n🔍 Nhập câu hỏi/nội dung cần tìm (hoặc gõ 'exit' để thoát): ")
        if query.lower() == 'exit':
            break

        if not query.strip():
            continue

        # Tìm kiếm 3 đoạn văn có nội dung tương đồng nhất với câu hỏi
        print("🕵️ Đang tìm kiếm thông tin tương quan...")
        results = vector_db.similarity_search(query, k=3)

        print(f"\n📌 Kết quả tìm thấy cho: '{query}'")
        for i, doc in enumerate(results, start=1):
            print(f"\n--- Đoạn trích {i} (Trang {doc.metadata.get('page', 0) + 1}) ---")
            print(doc.page_content.strip())
            print("-" * 30)


if __name__ == "__main__":
    main()

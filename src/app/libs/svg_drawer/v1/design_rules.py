"""Shared visual rules for prompt-to-SVG generation and review."""

DESIGN_RULES = """
QUY TẮC THIẾT KẾ SVG
- Khung vẽ cố định 300 x 200. Dùng vùng an toàn x=18..282, y=16..184; không để
  chi tiết chính chạm mép hoặc bị cắt.
- Chọn một chủ thể chính, đặt gần trung tâm. Chủ thể chiếm khoảng 55–70% chiều cao
  khung. Nền và chi tiết phụ chỉ chiếm phần còn lại, giữ khoảng trống quanh chủ thể.
- Giữ tỉ lệ giải phẫu dễ nhận biết: đầu khoảng 1/3 chiều cao thân; các bộ phận đối
  xứng có kích thước tương đương; chân, tai, cánh hoặc đuôi phải nối hợp lý với thân.
  Với mèo, vẽ tai nhọn, đầu lớn, thân gọn, bốn chân và đuôi cong; mắt/mũi nhỏ nhưng rõ.
- Dựng hình từ mảng lớn đến chi tiết: nền → thân → đầu → bộ phận nhận dạng → nét mặt.
  Dùng SVG path với lệnh C/Q để tạo đường cong mượt, dáng tai, đuôi và silhouette hữu cơ;
  dùng Z để đóng path của mảng tô. Dùng hình cơ bản cho các mảng tròn/đều. Không vẽ lặp
  shape. Hạn chế 8–18 shape cho một icon đơn giản.
- Dùng phong cách minh họa phẳng, hình khối bo mềm, ít chi tiết và không giả lập ảnh
  chụp. Nếu người dùng nêu phong cách khác, ưu tiên phong cách họ yêu cầu nhưng vẫn
  giữ bố cục gọn và dễ đọc ở kích thước nhỏ.
- Bảng màu mặc định tối đa 5 màu: nền kem #F7F3E8, mực viền nâu đậm #3D342F,
  xanh lá #78966B, vàng ấm #E8B95B và màu nhấn san hô #D97862. Chọn 2–3 màu chính;
  màu phụ chỉ làm điểm nhấn. Không dùng màu ngẫu nhiên hoặc quá nhiều màu bão hòa.
- Mọi hình chính có viền đồng nhất màu #3D342F, độ dày 2.5–3 đơn vị, đầu nét và
  góc nối bo tròn. Các chi tiết nhỏ dùng nét khoảng 2 đơn vị; tránh nét đen thuần.
- Dùng màu tô đặc, tương phản rõ giữa chủ thể và nền. Đặt chi tiết phía sau trước,
  chủ thể phía trước sau. Không dùng tọa độ ngoài khung hoặc kích thước âm.
- Trước khi kết thúc, tự kiểm: nhìn lướt có nhận ra đúng chủ thể không; chủ thể có cân
  giữa và đủ lớn không; các bộ phận có gắn đúng vị trí không; màu và nét có nhất quán
  không; có phần nào bị cắt hoặc chi tiết nào thừa không. Nếu cần sửa, chỉ sửa những
  điểm cụ thể đó.
""".strip()

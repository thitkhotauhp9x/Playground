import numpy as np
from pyefd import elliptic_fourier_descriptors, reconstruct_contour

import numpy as np


import numpy as np
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def generate_random_points_ordered_by_time(n, noise_level=0.2):
    # 1. Sinh chuỗi thời gian t tăng dần đều
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)

    # 2. Tạo một hình nền cơ sở (ví dụ: hình tròn bán kính 5)
    base_radius = 5.0
    x_base = base_radius * np.cos(t)
    y_base = base_radius * np.sin(t)

    # 3. Thêm nhiễu ngẫu nhiên vào tọa độ để tạo hình thù dị dạng ngẫu nhiên
    # (Nhưng vẫn giữ được dòng chảy tuần tự của t)
    x_noise = np.random.uniform(-noise_level, noise_level, n)
    y_noise = np.random.uniform(-noise_level, noise_level, n)

    x = x_base + x_noise
    y = y_base + y_noise

    # Trả về mảng chứa cấu trúc: [t, x, y]
    return np.column_stack((x, y))


# Tạo 200 điểm sắp xếp theo thời gian t



def d1(points):
    # import pdb; pdb.set_trace()
    coeffs = elliptic_fourier_descriptors(points, order=20)
    approx = reconstruct_contour(coeffs, num_points=500)

    # Vẽ kết quả
    import matplotlib.pyplot as plt

    plt.plot(*np.vstack([points, points[0]]).T, "o--", label="Điểm ban đầu")
    plt.plot(approx[:, 0], approx[:, 1], label="Xấp xỉ Fourier")
    plt.axis("equal")
    plt.legend()
    plt.show()


# 1. Định nghĩa cấu trúc dữ liệu đầu ra mong muốn từ LLM bằng Pydantic
class FourierConfig(BaseModel):
    action: str = Field(
        description="Hành động xử lý hình ảnh dựa trên prompt (ví dụ: 'smooth', 'scale', 'rotate', 'keep_as_is')")
    num_coefficients: int = Field(
        description="Số lượng hệ số Fourier (N) muốn giữ lại. Hình phức tạp cần N lớn (ví dụ: 50-100), hình đơn giản cần N nhỏ (ví dụ: 10-20).")
    transformation_matrix: List[List[float]] = Field(
        description="Ma trận biến đổi 2x2 [[cos(a), -sin(a)], [sin(a), cos(a)]] nếu prompt yêu cầu xoay hoặc phóng to, nếu không thì để ma trận đơn vị [[1.0, 0.0], [0.0, 1.0]].")


# 2. Hàm tính toán chuỗi Fourier (DFT) và tái tạo lại các điểm (X, Y)
def compute_fourier_points(points: np.ndarray, num_coeffs: int) -> np.ndarray:
    """
    Biến đổi các điểm (x, y) thành dạng số phức, tính DFT,
    giữ lại num_coeffs hệ số quan trọng nhất và nghịch đảo (IDFT) để tạo ra tọa độ (X, Y) mới.
    """
    # Chuyển tọa độ (x, y) thành chuỗi số phức z = x + iy
    z = points[:, 0] + 1j * points[:, 1]

    # Tính toán Discrete Fourier Transform (DFT)
    z_fft = np.fft.fft(z)

    # Lọc bỏ các tần số cao để làm mịn hoặc khớp theo cấu hình (Giữ lại N hệ số)
    # Lấy các hệ số ở đầu và cuối chuỗi (tần số thấp)
    filtered_fft = np.zeros_like(z_fft)
    half_coeffs = min(num_coeffs // 2, len(z_fft) // 2)

    filtered_fft[:half_coeffs] = z_fft[:half_coeffs]
    filtered_fft[-half_coeffs:] = z_fft[-half_coeffs:]

    # Nghịch đảo Fourier (IDFT) để lấy lại tập hợp điểm (X, Y) đã được xử lý bằng chuỗi Fourier
    z_reconstructed = np.fft.ifft(filtered_fft)

    # Trả về mảng các điểm (X, Y)
    X = np.real(z_reconstructed)
    Y = np.imag(z_reconstructed)
    return np.column_stack((X, Y))


# 3. Luồng xử lý chính kết hợp LangChain và OpenAI
def generate_fourier_shape(input_points: List[Dict[str, float]], prompt_text: str) -> List[Dict[str, float]]:
    # Khởi tạo OpenAI Model (Đảm bảo bạn đã export OPENAI_API_KEY)
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Thiết lập Parser dựa trên Pydantic
    parser = JsonOutputParser(pydantic_object=FourierConfig)

    # Thiết lập Prompt Template cho LangChain
    prompt_template = ChatPromptTemplate.from_template(
        "Bạn là một chuyên gia toán học và xử lý tín hiệu.\n"
        "Đầu vào của bạn là một tập hợp các điểm dữ liệu hình dáng và một yêu cầu vẽ hình.\n"
        "Yêu cầu từ người dùng: {user_prompt}\n\n"
        "Hãy phân tích yêu cầu cấu hình chuỗi Fourier phù hợp.\n"
        "{format_instructions}"
    )

    # Tạo chuỗi xử lý (Chain)
    chain = prompt_template | model | parser

    # Gọi OpenAI để lấy cấu hình tối ưu cho chuỗi Fourier
    response_config = chain.invoke({
        "user_prompt": prompt_text,
        "format_instructions": parser.get_format_instructions()
    })

    print("--- Cấu hình đề xuất từ AI ---")
    print(json.dumps(response_config, indent=2))

    # Chuyển đổi dữ liệu điểm đầu vào thành Numpy Array
    points_array = np.array([[p['x'], p['y']] for p in input_points])

    # Áp dụng ma trận biến đổi từ LLM nếu có (Xoay, Phóng to/Thu nhỏ)
    matrix = np.array(response_config['transformation_matrix'])
    transformed_points = points_array @ matrix.T

    # import pdb; pdb.set_trace()
    # Tính toán tọa độ (X, Y) qua chuỗi Fourier
    num_coeffs = response_config['num_coefficients']
    output_points_array = compute_fourier_points(transformed_points, num_coeffs)

    # Định dạng lại đầu ra thành danh sách các điểm (X, Y)
    output_points = [{"X": float(pt[0]), "Y": float(pt[1])} for pt in output_points_array]

    return output_points


# --- VÍ DỤ SỬ DỤNG ---
if __name__ == "__main__":
    # Giả lập tập hợp các điểm đầu vào (Hình vuông bị nhiễu răng cưa)
    # Trong thực tế, đây là tập hợp điểm (x,y) bạn truyền vào
    # t = np.linspace(0, 2 * np.pi, 100)
    # x_input = np.sign(np.cos(t)) + np.random.normal(0, 0.05, 100)
    # y_input = np.sign(np.sin(t)) + np.random.normal(0, 0.05, 100)

    # d1(list(zip(x_input, y_input)))
    sample_points = generate_random_points_ordered_by_time(n=200, noise_level=0.5)
    d1(sample_points)

    sample_points = [{"x": x, "y": y} for x, y in sample_points]

    # Prompt yêu cầu vẽ hình từ người dùng
    user_prompt = "Hãy làm mịn các đường nét răng cưa này để vẽ thành một hình tròn mượt mà bằng chuỗi Fourier."

    # Chạy hàm
    result_points = generate_fourier_shape(sample_points, user_prompt)

    print("\n--- Đã tạo thành công tọa độ (X, Y) qua chuỗi Fourier ---")
    print(f"Số lượng điểm đầu ra: {len(result_points)}")
    print(f"Ví dụ 3 điểm đầu tiên: {result_points[:3]}")
    points = []
    for item in result_points:
        x = item["X"]
        y = item["Y"]
        points.append((x, y))
    d1(points)
    import pdb; pdb.set_trace()
    pass

# def d2():
#     import cv2
#
#     # Đọc ảnh từ đường dẫn
#     image = cv2.imread('i1.jpg')
#
#     # Chuyển đổi sang ảnh xám
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Làm mờ ảnh để khử nhiễu
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#
#     # Trích xuất biên cạnh vật thể bằng thuật toán Canny
#     edges = cv2.Canny(blurred, 100, 200)
#
#     # Hiển thị ảnh kết quả biên cạnh
#     cv2.imshow('Object Edges', edges)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# def d3():
#     import cv2
#
#     image = cv2.imread('i1.jpg')
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Tăng cường chi tiết vùng tối và sáng bằng CLAHE
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(gray)
#
#     # Giảm nhẹ độ mờ để tránh làm nhòe chi tiết nhỏ
#     blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
#
#     # Hạ thấp ngưỡng Canny xuống 50 và 150
#     edges = cv2.Canny(blurred, 50, 150)
#
#     cv2.imshow('Detailed Edges', edges)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#
# if __name__ == "__main__":
#     d1()

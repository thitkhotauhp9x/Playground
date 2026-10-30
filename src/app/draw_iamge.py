import numpy as np
from pyefd import elliptic_fourier_descriptors, reconstruct_contour

def d1():
    points = [
        (0.00, 3.50),   # đỉnh đầu
        (-0.32, 3.38), (-0.48, 3.12), (-0.45, 2.82),
        (-0.25, 2.58),  # cổ bên trái
        (-0.48, 2.48),  # vai trái
        (-1.20, 1.72), (-1.05, 1.54),  # tay trái, bàn tay
        (-0.42, 2.12),  # nách trái
        (-0.34, 1.35),  # thân bên trái
        (-0.58, 0.72),  # hông trái
        (-0.52, 0.12), (-0.68, -0.72), (-0.28, -0.72),  # chân trái
        (0.00, 0.05),   # khoảng giữa hai chân
        (0.28, -0.72), (0.68, -0.72), (0.52, 0.12),  # chân phải
        (0.58, 0.72),   # hông phải
        (0.34, 1.35),   # thân bên phải
        (0.42, 2.12),   # nách phải
        (1.05, 1.54), (1.20, 1.72),  # bàn tay, tay phải
        (0.48, 2.48),   # vai phải
        (0.25, 2.58),   # cổ bên phải
        (0.45, 2.82), (0.48, 3.12), (0.32, 3.38),
    ]

    coeffs = elliptic_fourier_descriptors(points, order=20)
    approx = reconstruct_contour(coeffs, num_points=500)

    # Vẽ kết quả
    import matplotlib.pyplot as plt

    plt.plot(*np.vstack([points, points[0]]).T, "o--", label="Điểm ban đầu")
    plt.plot(approx[:, 0], approx[:, 1], label="Xấp xỉ Fourier")
    plt.axis("equal")
    plt.legend()
    plt.show()


def d2():
    import cv2

    # Đọc ảnh từ đường dẫn
    image = cv2.imread('i1.jpg')

    # Chuyển đổi sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm mờ ảnh để khử nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Trích xuất biên cạnh vật thể bằng thuật toán Canny
    edges = cv2.Canny(blurred, 100, 200)

    # Hiển thị ảnh kết quả biên cạnh
    cv2.imshow('Object Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def d3():
    import cv2

    image = cv2.imread('i1.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Tăng cường chi tiết vùng tối và sáng bằng CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Giảm nhẹ độ mờ để tránh làm nhòe chi tiết nhỏ
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Hạ thấp ngưỡng Canny xuống 50 và 150
    edges = cv2.Canny(blurred, 50, 150)

    cv2.imshow('Detailed Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    d3()

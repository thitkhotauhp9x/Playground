# Playground

## Yêu cầu

- Python `>=3.13,<4.0`
- Poetry 2.x

## Cài đặt môi trường

Tại thư mục dự án, chạy:

```powershell
poetry install
```

Poetry tạo virtual environment trong thư mục `.venv` của dự án (đã được Git bỏ qua). Để mở shell trong môi trường:

```powershell
poetry env activate
```

Hoặc chạy lệnh Python trực tiếp mà không cần kích hoạt shell:

```powershell
poetry run python --version
poetry run python -m pip list
```

## Chạy mã nguồn

Các module nằm trong `src/playground`. Sau khi cài dependencies, chạy module cần thiết bằng `poetry run`, ví dụ:

```powershell
poetry run python -m playground.chat
```

Lưu ý: source hiện có import các module `hat.*`, nhưng package chứa các module đó chưa được khai báo trong `pyproject.toml`. Cần bổ sung/cài dependency tương ứng trước khi chạy những module phụ thuộc vào `hat`.

## Tạo SVG từ prompt

Đặt OpenAI API key trong biến môi trường. Trong PowerShell, thiết lập tạm cho phiên hiện tại:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Tạo ảnh SVG bằng lệnh:

```powershell
poetry run playground-svg "A friendly orange cat sitting under a starry night sky" --output images/cat.svg
```

Có thể chọn model khác bằng `--model`, ví dụ `--model gpt-4o`. SVG mặc định được lưu tại `output.svg` nếu không truyền `--output`. Không commit API key vào repository.

## Quản lý dependencies

Thêm dependency runtime:

```powershell
poetry add <package>
```

Thêm dependency chỉ dùng khi phát triển:

```powershell
poetry add --group dev <package>
```

Đồng bộ môi trường theo lockfile:

```powershell
poetry sync
```

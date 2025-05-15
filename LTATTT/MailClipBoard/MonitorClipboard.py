import win32gui, win32api, ctypes
from win32clipboard import GetClipboardOwner, GetClipboardData
from win32process import GetWindowThreadProcessId
from psutil import Process

allowlist = ["notepad.exe", "python.exe", "code.exe"]

def processEvent(hwnd, msg, wparam, lparam):
    if msg == 0x031D:  # Kiểm tra sự kiện clipboard thay đổi (message ID 0x031D)
        try:
            win = GetClipboardOwner()  # Lấy tiến trình sở hữu clipboard
            pid = GetWindowThreadProcessId(win)[1]  # Lấy PID của tiến trình
            p = Process(pid)  # Lấy đối tượng tiến trình từ PID
            name = p.name()  # Lấy tên của tiến trình
            if name not in allowlist:  # Kiểm tra nếu tiến trình không nằm trong danh sách cho phép
                print("Clipboard modified by %s" % name)
                
                # Lấy nội dung của clipboard và in ra
                win32clipboard.OpenClipboard()
                clipboard_content = win32clipboard.GetClipboardData()  # Lấy nội dung clipboard
                print("Clipboard content: %s" % clipboard_content)  # In ra nội dung clipboard
                win32clipboard.CloseClipboard()
        except Exception as e:
            print("Clipboard modified by unknown process")
            print("Error: ", str(e))
    return 0  # Trả về 0 để Windows tiếp tục xử lý

# Hàm tạo cửa sổ ẩn để lắng nghe sự kiện clipboard
def createWindow():
    wc = win32gui.WNDCLASS()  # Tạo lớp cửa sổ
    wc.lpfnWndProc = processEvent  # Gán hàm xử lý sự kiện vào lớp cửa sổ
    wc.lpszClassName = 'clipboardListener'  # Đặt tên cho lớp cửa sổ
    wc.hInstance = win32api.GetModuleHandle(None)  # Lấy handle của chương trình hiện tại
    class_atom = win32gui.RegisterClass(wc)  # Đăng ký lớp cửa sổ
    return win32gui.CreateWindow(class_atom, 'clipboardListener', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)  # Tạo cửa sổ

# Hàm thiết lập listener để lắng nghe sự kiện clipboard
def setupListener():
    hwnd = createWindow()  # Tạo cửa sổ listener
    ctypes.windll.user32.AddClipboardFormatListener(hwnd)  # Thêm cửa sổ vào danh sách các cửa sổ lắng nghe clipboard
    win32gui.PumpMessages()  # Lắng nghe và xử lý các sự kiện (chạy chương trình chính)

setupListener()  # Gọi hàm thiết lập listener để bắt đầu giám sát clipboard

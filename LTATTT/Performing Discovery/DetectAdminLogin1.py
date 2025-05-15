import win32evtlog

# Máy chủ cần kiểm tra (localhost tức là máy đang chạy script)
server = "localhost"

# Loại log cần kiểm tra: Security (ghi lại các sự kiện bảo mật như đăng nhập)
logtype = "Security"

# Cờ đọc log: theo thứ tự, đọc từ đầu đến cuối
flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

# Hàm đọc các sự kiện có ID nhất định từ Event Log hoặc file backup
def QueryEventLog(eventID, filename=None):
    logs = []
    # Nếu không có file backup, đọc từ log trực tiếp
    if not filename:
        h = win32evtlog.OpenEventLog(server, logtype)
    else:
        h = win32evtlog.OpenBackupEventLog(server, filename)
    
    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        if not events:
            break
        for event in events:
            if event.EventID & 0xFFFF == eventID:  # Chỉ lấy phần thấp 16 bit của Event ID
                logs.append(event)
    return logs

# Hàm kiểm tra đăng nhập đặc quyền (Event ID 4672)
def DetectAdministratorLogin():
    events = QueryEventLog(4672)
    for event in events:
        # Lọc những sự kiện có SID người dùng thông thường (bắt đầu bằng "S-1-5-21")
        if event.StringInserts and event.StringInserts[0].startswith("S-1-5-21"):
            username = event.StringInserts[1]
            logon_time = event.TimeGenerated
            privileges = event.StringInserts[-1]
            print(f"[!] Login with admin privileges:")
            print(f" -> User: {username}")
            print(f" -> Time: {logon_time}")
            print(f" -> Privileges: {privileges}\n")

# Gọi hàm chính
DetectAdministratorLogin()

#chạy quyền admin trên powershell

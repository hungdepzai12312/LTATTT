import winreg  # Thư viện tích hợp để thao tác với Registry của Windows

# Hàm kiểm tra xem trong một khóa registry (đã mở) có tồn tại một giá trị có tên là 'keyword' không
def checkValues(key, keyword):
    numValues = winreg.QueryInfoKey(key)[1]  # Lấy số lượng giá trị (values) trong khóa (vị trí [1] trả về số values)
    for i in range(numValues):  # Duyệt qua tất cả các value trong khóa
        try:
            values = winreg.EnumValue(key, i)  # Lấy thông tin của value tại chỉ số i (trả về tuple: (name, data, type))
            if values[0] == keyword:  # Nếu tên value trùng với keyword đang tìm
                return values[1]      # Trả về dữ liệu (data) của value đó
        except Exception as e:
            continue  # Bỏ qua nếu có lỗi (ví dụ value bị lỗi, không thể đọc)
    return None  # Không tìm thấy giá trị cần tìm

# Hàm kiểm tra tất cả các user trong hệ thống xem có logon script nào được thiết lập không
def checkLogonScripts():
    try:
        # Lấy số lượng khóa con (user SID) trong HKEY_USERS — mỗi khóa là một người dùng
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
    except Exception as e:
        print(e)
        return  # Thoát nếu không thể truy cập HKEY_USERS

    # Duyệt qua tất cả các user (qua SID)
    for i in range(numUsers):
        try:
            userKey = winreg.EnumKey(winreg.HKEY_USERS, i)  # Lấy tên khóa con thứ i, thường là SID của user
            regPath = "%s\\%s" % (userKey, "Environment")   # Xây dựng đường dẫn đến khóa Environment của user đó
            key = winreg.OpenKey(winreg.HKEY_USERS, regPath)  # Mở khóa Environment

            # Kiểm tra xem trong khóa này có tồn tại giá trị "UserInitMprLogonScript" không
            script = checkValues(key, "UserInitMprLogonScript")
            if script:
                # Nếu có, in ra đường dẫn và nội dung script
                print("Logon script detected at HKU\\%s\\Environment:\n\t%s" % (userKey, script))
        except:
            continue  # Bỏ qua nếu có lỗi (ví dụ khóa không tồn tại, không có quyền truy cập,...)

# Gọi hàm chính để kiểm tra logon scripts trên hệ thống
checkLogonScripts()
#Đoạn mã này dùng để kiểm tra xem trong registry của Windows có tồn tại logon script nào cho người dùng hay không,
#thông qua khóa UserInitMprLogonScript trong HKEY_USERS\<UserSID>\Environment

#cách chạy code này là thêm một key logon script vào bằng cách mở pwshell với quyền admin và gõ :Set-ItemProperty -Path "HKCU:\Environment" -Name "UserInitMprLogonScript" -Value "C:\test\myscript.bat"
#để gỡ dùng lệnh : Remove-ItemProperty -Path "HKCU:\Environment" -Name "UserInitMprLogonScript"

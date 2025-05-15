#Mục đích chính của đoạn mã này là thêm một logon script vào registry của một người dùng cụ thể, 
#để khi người dùng đăng nhập vào hệ thống, một ứng dụng (ở đây là "notepad.exe") sẽ được tự động chạy
#Khi user có SID này đăng nhập vào hệ thống, Windows sẽ kiểm tra giá trị UserInitMprLogonScript trong Registry.
#Nếu có, nó sẽ chạy chương trình được chỉ định (ở đây là notepad.exe).
import winreg  # Nhập thư viện làm việc với registry của Windows

# Thiết lập khóa registry cần chỉnh sửa
# Nếu muốn chỉnh cho user hiện tại thì dùng HKEY_CURRENT_USER, ở đây chúng ta dùng HKEY_USERS để chỉ rõ một user cụ thể qua SID
reghive = winreg.HKEY_USERS  # Hive chính trong registry: HKEY_USERS chứa thông tin của tất cả người dùng
userSID = "S-1-5-21-2684995931-2889235137-1778496725-1001"  # SID (Security Identifier) của người dùng cụ thể
regpath = userSID + "\\Environment"  # Đường dẫn đến khóa chứa các biến môi trường của user

command = "notepad.exe"  # Lệnh sẽ được chạy khi người dùng đăng nhập

# Mở khóa registry với quyền ghi (WRITE) để có thể chỉnh sửa
key = winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_WRITE)

# Ghi giá trị "UserInitMprLogonScript" vào khóa trên với nội dung là lệnh cần chạy
# Điều này sẽ khiến notepad.exe được tự động chạy khi user tương ứng đăng nhập vào Windows
winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, command)

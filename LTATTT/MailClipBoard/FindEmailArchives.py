import glob, os
import glob, os
import glob, os
from zipfile import ZipFile
from sys import platform

# Hàm tìm kiếm các file có phần mở rộng được cung cấp
def findFiles(extensions):
    files = []
    for ext in extensions:
        # Xác định mẫu tìm file phù hợp với hệ điều hành
        if platform == "win32":
            pattern = r"~\**\*."+ext     # Với Windows: tìm từ thư mục người dùng
        else:
            pattern = r"~/**/*."+ext     # Với Linux/macOS
        pattern = os.path.expanduser(pattern)  # Mở rộng ký hiệu ~ thành thư mục người dùng hiện tại

        # Tìm tất cả các file khớp với mẫu (đệ quy toàn bộ thư mục con)
        f = glob.glob(pattern, recursive=True)

        # Nếu là file nén (zip), cần kiểm tra bên trong có chứa file email hay không
        if ext in archiveFiles:
            for a in f:
                if searchArchiveFile(a):
                    files.append(a)     # Nếu có chứa file email, thêm vào danh sách
        else:
            files += f                 # Nếu là file .pst, .ost thì thêm trực tiếp
    return files

# Danh sách phần mở rộng của file nén (để kiểm tra nội dung bên trong)
archiveFiles = ["zip"]

# Hàm kiểm tra một file .zip có chứa file email (.pst, .ost) không
def searchArchiveFile(filename):
    try:
        for file in ZipFile(filename, "r").namelist():
            email = True in [file.endswith(ext) for ext in emailFiles]  # Kiểm tra từng file trong zip
            if email:
                return True
    except:
        return False
    return False

# Danh sách phần mở rộng của file email
emailFiles = ["pst", "ost"]

# Kết hợp danh sách mở rộng cần tìm: gồm file email và file nén
extensions = emailFiles + archiveFiles

# In ra các file tìm được
print("Email archives:")
for f in findFiles(extensions):
    print("\t%s" % f)
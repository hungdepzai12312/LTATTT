import pathlib
import os

# Hàm lấy thông tin thời gian của file
def getTimestamps(filename):
    fname = pathlib.Path(filename)
    
    if not fname.exists():  # Kiểm tra nếu file không tồn tại
        print(f"File {filename} không tồn tại!")
        return []  # Trả về danh sách rỗng nếu file không tồn tại

    stats = fname.stat()
    return (stats.st_ctime, stats.st_mtime, stats.st_atime)

# Hàm tạo file decoy (file giả mạo)
def createDecoyFiles(filenames):
    with open("decoys.txt", "w", encoding="utf-8") as f:
        for file in filenames:
            if os.path.exists(file):  # Kiểm tra nếu file tồn tại
                (ctime, mtime, atime) = getTimestamps(file)
                f.write("%s,%s,%s,%s\n" % (file, ctime, mtime, atime))
            else:
                print(f"Không tìm thấy file: {file}")  # In ra nếu file không tồn tại

# Danh sách các file giả mạo (hãy thay đường dẫn bằng đường dẫn chính xác)
decoys = [
    r"E:\HK2NAM3\Lập trình ATTT\DS_MTAEduVn.py",
    r"E:\HK2NAM3\Lập trình ATTT\DS_QDND.py",
    r"E:\HK2NAM3\Lập trình ATTT\Ex.txt"
]

createDecoyFiles(decoys)

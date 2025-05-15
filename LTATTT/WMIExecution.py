import subprocess,wmi#Dùng để chạy các lệnh hệ thống hoặc PowerShell từ Python

def WMIProcessCreation(name):
    c = wmi.WMI()
    processID,returnValue = c.Win32_process.Create(CommandLine=name)#Gọi phương thức Create() của lớp Win32_Process để tạo một tiến trình với dòng lệnh name (ví dụ: "notepad.exe").
    print("Process %s created with PID %d" %(name,(processID)))
    
def PSProcessCreation(name):
    command = ["powershell","& { invoke-wmimethod win32_process -name create -argumentlist notepad.exe | select ProcessId | % { $_.ProcessId } | Write-Host }"]
    p = subprocess.run(command,shell=True,capture_output=True)
    #Thực thi lệnh PowerShell trên bằng subprocess.run, với:

#shell=True: Chạy trong shell.

#capture_output=True: Bắt stdout và stderr.
    if p.returncode == 0:
        print("Process %s created with PowerShell, PID %d" % (name, p.stdout.decode("utf-8")))

command = "notepad.exe"

WMIProcessCreation(command)
PSProcessCreation(command)
#Đoạn mã này thực hiện việc tạo một tiến trình mới (ở đây là "notepad.exe") trên hệ thống Windows bằng hai cách khác nhau:

#Sử dụng WMI (Windows Management Instrumentation) để tạo tiến trình.

#Sử dụng PowerShell để tạo tiến trình.
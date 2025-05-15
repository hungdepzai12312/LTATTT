from subprocess import check_output, CalledProcessError
import re

def checkLastLogin(user):
    try:
        # Dùng dấu ngoặc kép nếu tên user có khoảng trắng
        command = f'net user "{user}"'
        res = check_output(command, shell=True)
        logon = re.findall(r"Last logon\s*([^\r\n]+)", res.decode("utf-8"))[0]
        if logon != "Never":
            print(f"{user} last logged in at {logon}")
        else:
            print(f"{user} has never logged in")
    except CalledProcessError:
        print(f"User '{user}' does not exist")

# Danh sách user có thật trên máy bạn
decoyAccounts = ["Administrator", "DefaultAccount", "Guest", "Phi Hung", "WDAGUtilityAccount"]

for user in decoyAccounts:
    checkLastLogin(user)

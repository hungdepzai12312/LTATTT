import os, wmi

w = wmi.WMI()

# Get list of Administrator Accounts
admins = None
for group in w.Win32_Group():
    if group.Name == "Administrators":
        users = group.associators(wmi_result_class="Win32_UserAccount")
        admins = [a.Name for a in users]
        
# List user accounts on device
for user in w.Win32_UserAccount():
    print("Username: %s" % user.Name)
    print("Administrator: %s" % (user.Name in admins))
    print("Disabled: %s" % user.Disabled)
    print("Domain: %s" % user.Domain)
    print("Local: %s" % user.LocalAccount)
    print("Password Changeable: %s"%user.PasswordChangeable)
    print("Password Expires: %s" % user.PasswordExpires)
    print("Password Required: %s" % user.PasswordRequired)
    print("\n")

# Print Windows Password Policy
print("Password Policy:")
print(os.system("net accounts"))


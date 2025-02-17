import ctypes
import tkinter as tk
from ctypes import wintypes
import time
import threading

user32 = ctypes.WinDLL("user32", use_last_error=True)

class CURSORINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("hCursor", ctypes.c_void_p),  
                ("ptScreenPos", wintypes.POINT)]

def is_text_cursor():
    cursor_info = CURSORINFO()
    cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
    
    if user32.GetCursorInfo(ctypes.byref(cursor_info)):
        text_cursor = user32.LoadCursorW(None, 32513)  # IDC_IBEAM
        return cursor_info.hCursor == text_cursor
    return False

def get_keyboard_language():
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    klid = user32.GetKeyboardLayout(thread_id)
    return "ㅎ" if klid & 0xFFFF == 0x0412 else "A"

def get_cursor_position():
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

root = tk.Tk()
root.overrideredirect(True)  
root.attributes("-topmost", True)  
root.attributes("-alpha", 0.7) 
label = tk.Label(root, font=("Arial", 12, "bold"), bg="black", fg="white", padx=5, pady=2)
label.pack()

def update_label():
    while True:
        if is_text_cursor():  
            lang = get_keyboard_language()
            x, y = get_cursor_position()
            root.geometry(f"+{x+10}+{y+15}")
            label.config(text=lang)
            root.deiconify() 
        else:
            root.withdraw() 
        time.sleep(0.001) 

threading.Thread(target=update_label, daemon=True).start()
root.mainloop()
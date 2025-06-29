import win32gui

def get_Window():
    Current = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(Current)

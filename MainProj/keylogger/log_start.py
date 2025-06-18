import logging
from info.config import KEYLOG_FILE

logging.basicConfig(
    filename=KEYLOG_FILE,
    level=logging.INFO,
    format='%(asctime)s: %(message)s'
)

def log_keystrokes(text: str):
    """Write keystroke text to the log file."""
    logging.info(text)

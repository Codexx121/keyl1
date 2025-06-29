import socket
from datetime import datetime

def get_systeminfo():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info = f"System Info at {now}\nHostname: {hostname}\nIP Address: {ip_address}\n"
    return info

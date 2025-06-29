import requests

SERVER_URL = "http://localhost:5000/log"

def send_log_to_server(content):
    try:
        requests.post(SERVER_URL, json={"content": content}, timeout=2)
    except:
        pass  

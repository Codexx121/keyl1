import subprocess
import re
from info.config import WIFI_FILE

IP_Info = subprocess.run(
            ['curl', 'ifconfig.co/json'], capture_output=True, text=True
        )
print(IP_Info.stdout)

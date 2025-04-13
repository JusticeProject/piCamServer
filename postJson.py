import requests
from datetime import datetime

current_time = datetime.now()

alert_data = {
    "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
    "location": "Home",
    "total_persons": 1,
}

try:
    requests.post("http://127.0.0.1:6515/update_detection", json=alert_data)
except requests.exceptions.RequestException as e:
    print(f"Failed to send detection data to server: {str(e)}")

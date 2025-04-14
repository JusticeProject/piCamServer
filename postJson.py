import requests

cmd_data = {
    "value1": 47,
    "value2": 82,
}

print("Sending JSON to server: " + str(cmd_data))
try:
    resp = requests.post("http://127.0.0.1:6515/new_command", json=cmd_data)
    print("Response:")
    print(resp)
    print("JSON in the Response:")
    print(resp.json())
except requests.exceptions.RequestException as e:
    print(f"Failed to send JSON to server: {str(e)}")

print("Getting JSON from server")
try:
    resp = requests.get("http://127.0.0.1:6515/get_status")
    print("Response:")
    print(resp)
    print("JSON in the Response:")
    print(resp.json())
except requests.exceptions.RequestException as e:
    print(f"Failed to get JSON from server: {str(e)}")

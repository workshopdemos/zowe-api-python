import requests
import getpass
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def create_payload(extra_data=None):
    """
    TODO: Task 6 - Implement a helper function to create the request payload.
    This function should include the common connection details (username, password, host, etc.)
    and merge them with any extra data (like hlq or dataset names).
    """
    # Get credentials from environment or prompt
    # Hint: username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    # Hint: password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    # Hint: host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    # Hint: port = int(os.getenv("MAINFRAME_PORT", 5010))
    # Hint: reject_unauthorized = os.getenv("MAINFRAME_REJECT_UNAUTHORIZED", "false").lower() == "true"

    payload = {
        "username": "", # Replace with username
        "password": "", # Replace with password
        "host": "", # Replace with host
        "port": 5010, # Replace with port
        "reject_unauthorized": "false" # Replace with reject_unauthorized
    }

    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    port = int(os.getenv("MAINFRAME_PORT", 5010))
    reject_unauthorized = False

    payload = {
        "username": username, "password": password, "host": host,
        "port": port, "reject_unauthorized": reject_unauthorized
    }
    if extra_data:
        payload.update(extra_data)
    print("payload", payload)
    return payload

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Define the datasets for manipulation
    input_ds = "cust001.cust.data"
    output_ds = "cust001.cust.obdata"

    hlq = os.getenv("MAINFRAME_USER") or input("Enter HLQ to list: ")
    list_payload = create_payload({"hlq": hlq})
    list_response = requests.post("http://localhost:5010/list-datasets", json=list_payload)
    print("Found datasets:", list_response.json().get("datasets", []))
        
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    response = requests.post("http://localhost:5010/manipulate", json=manipulate_payload)
    print(response.json().get("message", "Manipulation complete!"))
    
    download_payload = create_payload({"input_dataset": output_ds})
    download_response = requests.post("http://localhost:5010/download-dataset", json=download_payload)
    content = download_response.json().get("content", "")

    records = []
    for line in content.splitlines():
        if len(line) >= 1:
            records.append({
                "account": line[0:8].strip(), "bill": line[8:12].strip(),
                "name": line[12:42].strip(), "phone": line[42:52].strip(),
                "email": line[52:82].strip()
            })
    print(json.dumps(records, indent=2))
    
if __name__ == "__main__":
    main()

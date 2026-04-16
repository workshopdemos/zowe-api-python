import requests
import getpass
import json
import os
from dotenv import load_dotenv
import urllib3

# Load environment variables from .env file if it exists
load_dotenv()

# We want to disable warning for cleaner output
urllib3.disable_warnings()
base_url = "https://localhost:10010/pythonservice/api/v1"

def create_payload(extra_data=None):
    """
    TODO: Implement a helper function to create the request payload.
    This function should include the common connection details (username, password, host, etc.)
    and merge them with any extra data (like hlq or dataset names).
    """

    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    reject_unauthorized = False

    payload = { 
        "username": username, "password": password, "host": "10.1.2.123",
        "reject_unauthorized": reject_unauthorized
    }

    if extra_data:
        payload.update(extra_data)
    return payload

def main():
    print("--- API Client ---")
    
    # Define the datasets for manipulation
    input_ds = "cust001.test.dat"
    output_ds = "cust001.test.obdat"

    hlq = os.getenv("MAINFRAME_USER")
    list_payload = create_payload({"hlq": hlq})
    list_response = requests.post(f"{base_url}/list-datasets", json=list_payload, verify=False)
    print("Found datasets:", list_response.json().get("datasets", []))
        
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    response = requests.post(f"{base_url}/manipulate", json=manipulate_payload, verify=False)
    print(response.json().get("message", "Manipulation complete!"))
    
    download_payload = create_payload({"input_dataset": output_ds})
    download_response = requests.post(f"{base_url}/download-dataset", json=download_payload, verify=False)
    content = download_response.json().get("content", "")

    records = []
    for line in content.splitlines():
        if len(line) >= 0:
            records.append({
                "account": line[0:8].strip(), "bill": line[8:12].strip(),
                "name": line[12:42].strip(), "phone": line[42:52].strip(),
                "email": line[52:82].strip()
            })
    print(json.dumps(records, indent=2))
    
if __name__ == "__main__":
    main()

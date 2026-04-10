import requests
import getpass
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def create_payload(extra_data=None):
    """
    Helper function to create the request payload with credentials.
    """
    # Get credentials from environment or prompt
    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    host = os.getenv("MAINFRAME_HOST", "mstrsvw.lvn.broadcom.net")
    port = int(os.getenv("MAINFRAME_PORT", 449))
    reject_unauthorized = False

    payload = {
        "username": username,
        "password": password,
        "host": host,
        "port": port,
        "reject_unauthorized": reject_unauthorized
    }

    if extra_data:
        payload.update(extra_data)

    return payload

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Define the datasets for manipulation
    input_ds = "mcqth01.cust.data"
    output_ds = "mcqth01.cust.data3"

    # Task 1: List datasets for your HLQ
    print("\n--- Task 1: List Datasets ---")
    hlq = os.getenv("MAINFRAME_USER") or input("Enter HLQ to list: ")
    list_payload = create_payload({"hlq": hlq})
    
    try:
        response = requests.post("http://localhost:5010/list-datasets", json=list_payload)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error! Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection Error: {str(e)}")

    # Task 2: Manipulate and Upload Data
    print("\n--- Task 2: Manipulate and Upload Data ---")
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    
    try:
        response = requests.post("http://localhost:5010/manipulate", json=manipulate_payload)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error! Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection Error: {str(e)}")

    # Task 3: Download Manipulated Data as JSON
    print("\n--- Task 3: Download Manipulated Data as JSON ---")
    download_payload = create_payload({"input_dataset": output_ds})
    
    try:
        response = requests.post("http://localhost:5010/download-dataset", json=download_payload)
        if response.status_code == 200:
            data = response.json()
            content = data.get("content", "")
            print(json.dumps(content, indent=2))
        else:
            print(f"Error! Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection Error: {str(e)}")

if __name__ == "__main__":
    main()

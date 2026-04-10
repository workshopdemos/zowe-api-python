import requests
import getpass
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def create_payload(extra_data=None):
    """
    TODO: Implement a helper function to create the request payload.
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
        "reject_unauthorized": False # Replace with reject_unauthorized
    }

    # TODO: Merge extra_data into the payload if provided
    # Hint: if extra_data: payload.update(extra_data)

    return payload

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Define the datasets for manipulation
    input_ds = "ZOWEUSER.PUBLIC.PII.DATA"
    output_ds = "ZOWEUSER.PUBLIC.MANIPULATED.DATA"

    # TODO: Task 1 - List datasets for your HLQ
    # 1. Use the helper to create a payload with {"hlq": "YOUR_USER"}
    # 2. Send POST to http://localhost:5010/list-datasets
    # 3. Print the results
    
    # TODO: Task 2 - Manipulate data
    # 1. Use the helper to create a payload with input/output dataset names
    # 2. Send POST to http://localhost:5010/manipulate
    # 3. Print the results
    
    # TODO: Task 3 - Download manipulated data as JSON
    # 1. Use the helper to create a payload with {"input_dataset": output_ds}
    # 2. Send POST to http://localhost:5010/download-dataset
    # 3. Parse the response and display the content
    # Hint: records = []
    # Hint: for line in content.splitlines():
    # Hint:     if len(line) >= 82: records.append({"account": line[0:8].strip(), ...})
    
    print("TODO: Implement Task 1, 2, and 3 in main()")

if __name__ == "__main__":
    main()

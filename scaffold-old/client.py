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
    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    port = int(os.getenv("MAINFRAME_PORT", 5010))
    reject_unauthorized = os.getenv("MAINFRAME_REJECT_UNAUTHORIZED", "false").lower() == "true"

    payload = {
        "username": username,
        "password": password,
        "host": host,
        "port": port,
        "reject_unauthorized": reject_unauthorized
    }

    # TODO: Merge extra_data into the payload if provided
    if extra_data:
        payload.update(extra_data)

    return payload

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Define the datasets for manipulation
    input_ds = "ZOWEUSER.PUBLIC.PII.DATA"
    output_ds = "ZOWEUSER.PUBLIC.MANIPULATED.DATA"

    # TODO: Task 1 - List datasets for your HLQ
    # 1. Use the helper to create a payload with {"hlq": "YOUR_USER"}
    # 2. Send POST to http://localhost:5000/list-datasets
    # 3. Print the results
    
    # TODO: Task 2 - Manipulate data
    # 1. Use the helper to create a payload with input/output dataset names
    # 2. Send POST to http://localhost:5000/manipulate
    # 3. Print the results
    
    # TODO: Task 3 - Download manipulated data as JSON
    # 1. Use the helper to create a payload with {"input_dataset": output_ds}
    # 2. Send POST to http://localhost:5000/download-dataset
    # 3. Parse the response and display the content
    
    # TODO: Send the POST request to the service
    # Hint: Use requests.post("http://localhost:5000/manipulate", json=payload)
    response = None # Replace this
    
    # TODO: Print the response from the service
    if response and response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error!")
        if response:
            print(response.text)

if __name__ == "__main__":
    main()

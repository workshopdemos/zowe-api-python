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
        "username": username, "password": password, "reject_unauthorized": reject_unauthorized
    }
    print("payload", payload)
    if extra_data:
        payload.update(extra_data)
    return payload

def main():
    print("--- API Client ---")
    
    # Define the datasets for manipulation
    input_ds = "cust001.test.dat"
    output_ds = "cust001.test.you" # Update this with your name

    hlq = os.getenv("MAINFRAME_USER")
    list_payload = create_payload({"hlq": hlq})
    
if __name__ == "__main__":
    main()

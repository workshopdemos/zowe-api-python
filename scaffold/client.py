import requests
import getpass
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Prompt for username and password if not in environment variables
    username = os.getenv("MAINFRAME_USER")
    if not username:
        username = input("Enter Mainframe Username: ")
        
    password = os.getenv("MAINFRAME_PASSWORD")
    if not password:
        password = getpass.getpass("Enter Mainframe Password: ")
    
    # Define the host, port, input dataset, and output dataset
    host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    port = int(os.getenv("MAINFRAME_PORT", 5010))
    reject_unauthorized = os.getenv("MAINFRAME_REJECT_UNAUTHORIZED", "false").lower() == "true"
    
    input_ds = "ZOWEUSER.PUBLIC.PII.DATA"
    output_ds = "ZOWEUSER.PUBLIC.MANIPULATED.DATA"
    
    # Create the payload for the POST request
    payload = {
        "username": username,
        "password": password,
        "host": host,
        "port": port,
        "reject_unauthorized": reject_unauthorized,
        "input_dataset": input_ds,
        "output_dataset": output_ds
    }
    
    # TODO: Send the POST request to the service
    # Hint: Use requests.post("http://localhost:5000/manipulate", json=payload)
    # OR use "http://localhost:5000/manipulate-download" to get the data back directly
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

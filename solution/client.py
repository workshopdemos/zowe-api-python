import requests
import getpass
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def main():
    print("--- Mainframe Data Manipulator Client ---")
    
    # Get credentials from environment variables or prompt the user
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
    
    # Send the POST request to the service
    try:
        # Change the URL to "http://localhost:5000/manipulate-download" if you want the data back in the response
        url = "http://localhost:5000/manipulate"
        response = requests.post(url, json=payload)
        
        # Print the response from the service
        if response.status_code == 200:
            print("\nSuccess!")
            result = response.json()
            if "manipulated_content" in result:
                print("\nManipulated Content Received:")
                print("-" * 30)
                print(result["manipulated_content"])
                print("-" * 30)
            else:
                print(json.dumps(result, indent=2))
        else:
            print("\nError!")
            print(f"Status Code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the service. Is manipulator_service.py running?")

if __name__ == "__main__":
    main()

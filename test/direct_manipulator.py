import os
import getpass
from zowe.zos_files_for_zowe_sdk import Datasets
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def manipulate_data(content):
    """
    Removes SSN entirely in fixed-width COBOL data.
    Input: 93 chars, Output: 82 chars.
    """
    manipulated_lines = []
    for line in content.splitlines():
        # Ensure the line is padded to at least 93 chars to handle trailing spaces
        line = f"{line:<93}"
            
        account = line[0:8]
        bill = line[8:12]
        
        # Skip SSN (chars 12-22) and take the rest
        rest = line[23:93]
        
        new_line = f"{account}{bill}{rest}"
        manipulated_lines.append(new_line)
    
    return "\n".join(manipulated_lines)

def main():
    print("--- Standalone Mainframe Manipulator (Direct) ---")
    
    # Get credentials
    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    port = int(os.getenv("MAINFRAME_PORT", 5010))
    reject_unauthorized = os.getenv("MAINFRAME_REJECT_UNAUTHORIZED", "false").lower() == "true"
    
    input_ds = "ZOWEUSER.PUBLIC.PII.DATA"
    output_ds = "ZOWEUSER.PUBLIC.MANIPULATED.DATA"
    
    # Create Zowe Profile
    profile = {
        "host": host,
        "port": port,
        "user": username,
        "password": password,
        "rejectUnauthorized": not reject_unauthorized
    }
    
    try:
        print(f"Connecting to {host}...")
        datasets = Datasets(profile)
        
        local_input = "input_temp.txt"
        local_output = "output_temp.txt"
        
        print(f"Downloading {input_ds} to {local_input}...")
        datasets.perform_download(input_ds, local_input)
        
        print("Reading and manipulating data...")
        with open(local_input, "r") as f:
            content = f.read()
            
        manipulated_content = manipulate_data(content)
        
        with open(local_output, "w") as f:
            f.write(manipulated_content)
            
        print(f"Uploading {local_output} to {output_ds}...")
        datasets.perform_upload(local_output, output_ds)
        
        # Cleanup temporary files
        if os.path.exists(local_input):
            os.remove(local_input)
        if os.path.exists(local_output):
            os.remove(local_output)
        
        print("\nSuccess! Data has been manipulated and uploaded directly.")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()

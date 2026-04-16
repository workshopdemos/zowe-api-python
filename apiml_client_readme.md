# API Mediation Layer Client Guide

This client application acts as a bridge between your local environment and the **Python API Service**. Its primary goal is to automate the process of identifying, cleaning, and retrieving mainframe datasets that contain sensitive information.

---

## Overview

If you are running out of time, the completed version of this code is in the `completed_files/` folder. You can move it to the current directory using `mv completed_files/apiml_client.py ./` and then run it using `python apiml_client.py`.

---

## Core Program Logic

The application follows a logical progression of data management tasks. Each step interacts with a specific API endpoint provided by the service:

1. **Authentication and Credential Gathering**: Loads credentials from a `.env` file or securely prompts the user for their mainframe username and password.
2. **Listing User Datasets**: Queries the service for a list of all datasets associated with the user's High-Level Qualifier (HLQ).
3. **Triggering Data Manipulation (Cleaning)**: Sends a request to take a "dirty" input dataset (e.g., `cust001.test.dat`) and produce a "clean" version (e.g., `cust001.test.you`).
4. **Retrieving and Parsing Results**: Once cleaned, the results are stored in a new dataset on the mainframe. The client downloads the content and parses it from a fixed-width mainframe format into a modern, structured JSON format.

---

## Configuration Details

### The `.env` File
To avoid repetitive manual input, use a `.env` file in the project root. This file is read by `load_dotenv()` and populated into the script's environment.

**Action**: Ensure `.env` contains the following:

```bash
MAINFRAME_USER=cust001
MAINFRAME_PASSWORD=cust001
REJECT_UNAUTHORIZED=false
```

### Libraries Used
- **`requests`**: For making HTTP calls to the REST API.
- **`python-dotenv`**: For managing sensitive configuration variables.
- **`urllib3`**: Used here to suppress SSL warnings for local development environments.

---

## Step-by-Step Implementation Guide

Follow these steps to complete the logic within `apiml_client.py`.

### Task 1: Customizing Your Environment
Before you begin implementing the logic, you must define which datasets you want the service to work on.

**Action**: In `apiml_client.py`, locate the `main()` function and update the following variables. **Note**: Change `cust001.test.you` to something unique (like your name or initials) to avoid conflicting with other participants.

```python
    # Define the datasets for manipulation
    input_ds = "cust001.test.dat"
    output_ds = "cust001.test.you" # Update 'you' to your name or something unique
```

### Task 2: Implementing the `create_payload` Helper
Every API call to the manipulator service requires a set of base connection details. Instead of repeating this code, we use a helper function.

**Action**: Replace the contents of the `create_payload` function in `apiml_client.py` with this code:

```python
def create_payload(extra_data=None):
    # Fetch credentials from environment or user input
    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    reject_unauthorized = False

    # Base payload structure
    payload = {
        "username": username,
        "password": password,
        "reject_unauthorized": reject_unauthorized
    }
    
    # Merge with specific request parameters
    if extra_data:
        payload.update(extra_data)
        
    return payload
```

### Task 3: Implementing the Main Workflow
This is the "brain" of your client where the sequence of operations is executed.

**Action**: Copy the following logic into the `main()` function after the payload is initialized in `apiml_client.py`:

```python
    # 1. List Datasets: Verify access and see what exists
    hlq = os.getenv("MAINFRAME_USER")
    list_payload = create_payload({"hlq": hlq})
    list_response = requests.post(f"{base_url}/list-datasets", json=list_payload, verify=False)
    print("Found datasets:", list_response.json().get("datasets", []))
        
    # 2. Trigger Manipulation: Create the cleaned dataset
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    response = requests.post(f"{base_url}/manipulate", json=manipulate_payload, verify=False)
    print(response.json().get("message", "Manipulation complete!"))
    
    # 3. Download and Parse: Retrieve the cleaned data
    download_payload = create_payload({"input_dataset": output_ds})
    download_response = requests.post(f"{base_url}/download-dataset", json=download_payload, verify=False)
    content = download_response.json().get("content", "")

    # Convert fixed-width mainframe format to structured JSON
    records = []
    for line in content.splitlines():
        if len(line) >= 0: # Ensure line contains all expected fields
            records.append({
                "account": line[0:8].strip(),
                "bill": line[8:12].strip(),
                "name": line[12:42].strip(),
                "phone": line[42:52].strip(),
                "email": line[52:82].strip()
            })
    print(json.dumps(records, indent=2))
```

---

## Running the Application

**Action**:
Run the following command in your terminal:
```bash
python apiml_client.py
```

**Expected Result**:
You should see a list of datasets, a success message, and a JSON dump of the cleaned data:
```text
--- Mainframe Data Manipulator Client ---
Found datasets: ['CUST001.DATA1', 'CUST001.TEST.DAT', ...]
Data manipulated and uploaded
[
  {
    "account": "90825067",
    "bill": "1679",
    "name": "Kenneth Davis",
    "phone": "4514282286",
    "email": "kenneth.davis410@icloud.com"
  },
  ...
]
```

---

## Congratulations!
You've successfully completed the workshop and gained the knowledge to create your own APIs integrated with the Zowe API Mediation Layer.


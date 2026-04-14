# Workshop: Mainframe Data Manipulation with Python

Welcome! In this workshop, you will build a Python service that connects to a mainframe, downloads a dataset, removes Social Security Numbers (SSN) entirely, and uploads the "clean" data back.

## Why are we doing this?

Mainframes hold the world's most sensitive data. Traditionally, accessing this data required 3270 terminals. By using Python and the Zowe SDK, we can:

1.  **Modernize Access**: Interact with the mainframe using standard REST APIs.
2.  **Automate Compliance**: Programmatically remove sensitive information before it ever leaves the secured environment.
3.  **Bridge the Gap**: Allow modern web applications to safely consume mainframe data in formats like JSON.

While we are reusing the Zowe APIs, we can also use them to create additional functionality. In this case, we are manipulating the data. This could be anything, such as capturing specific output, combining output, reformatting it to another useful format, or even building complex logic and integrations.

This workshop focuses on:
- Using Python to integrate with the Zowe APIs.
- Learning how to publish APIs (useful if integrating with Zowe API Mediation Layer).
- Creating a client to interact with the newly created APIs.
- Managing credentials securely.

---

## Step 1: Install the Tools (5 minutes)

First, we need to install the Python libraries that do the heavy lifting. This command installs all the dependencies (additional libraries) so we can focus on the solution.

1.  **Open your terminal**:
    - Open a new terminal via the **Terminal** menu or the "hamburger" (three horizontal lines) menu in the top-left.
    - Select **Terminal** > **New Terminal**.
2.  **Navigate to the `scaffold/` folder**:
    ```bash
    cd scaffold
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Step 2: Set Your Credentials (2 minutes)

We need to tell the code how to log in to your mainframe. You can use the file navigator to rename the file or use the terminal:

1.  Find the file named `.env.example`.
2.  Rename it to exactly `.env` (e.g., `mv .env.example .env` in the terminal).
3.  Open `.env` and replace `your_username` and `your_password` with your real mainframe credentials.
4.  Save the file.

---

## Important Notes - Python Conventions

Python uses **indentation** to define logic blocks. Everything in the same block must be at the same indentation level. If you are copying and pasting code, ensure the indentation remains consistent. You can use the **TAB** key to indent blocks of code. Note that spaces and tabs should not be mixed; for this workshop, we will use standard 4-space indentation (or the TAB key).

### Conventions:

#### Imports
```python
from flask import Flask, request, jsonify
from zowe.zos_files_for_zowe_sdk import Datasets, DatasetOption
import logging
import os
```
- These lines import external libraries into the application for use.
- `Flask` is our web framework, and the `zowe` library provides mainframe connectivity.

#### Functions
```python
def name(parameter):
    # Code goes here
```
- This defines a function. All code belonging to the function must be indented (usually 1 TAB or 4 spaces).
- See line 11 in `manipulator_service.py` for an example.

#### Comments
Multi-line comments (docstrings) are defined with three double-quotes (`"""`) at the start and end:
```python
"""
This is a multi-line comment.
"""
```
- In-line comments start with a hash sign (`#`). Everything after the `#` on that line is ignored by Python.

#### Returning Data
```python
return data
```
- This indicates the value the function should send back to the caller.

#### String Slicing
```python
string[0:8]
```
- This captures a portion of a string (in this case, the first 8 characters).

#### Lists and List Comprehensions
```python
names = [item.name for item in items]
```
- `[` and `]` define a list.
- The example above is a "list comprehension," a concise way to create a new list from an existing one.

#### Try/Except Blocks
```python
try:
    # Code to attempt
except Exception as e:
    # Code to run if an error occurs
```
- This is used for error handling to prevent the application from crashing.

#### Decorators
```python
@app.route('/list-datasets', methods=['POST'])
```
- Decorators modify the behavior of the function immediately following them.
- In Flask, `@app.route` maps a URL (endpoint) to a specific Python function.

---

## Phase 1: Server Implementation (`manipulator_service.py`)

In this phase, we will build the "brain" of our service. We'll implement the manipulation logic, the dataset allocation helper, and the API endpoints.

### Step 3: Task 1 - Implement Manipulation Logic
**Goal**: Create the logic that strips SSNs from fixed-width COBOL data.

1.  Open `manipulator_service.py`.
2.  Find the `manipulate_data` function (around line 32).
3.  Replace the `TODO: Task 1` sections inside the `for` loop with this code:
    ```python
        # Remove SSN (chars 12-22) by skipping them
        rest = line[23:93]
        
        # Reconstruct the fixed-width line without SSN
        new_line = f"{account}{bill}{rest}"
    ```
**Why?** Mainframe data is often "fixed-width," meaning every field starts and ends at an exact character position. By slicing the string to skip the SSN positions, we create a new, safe record format.

### Step 4: Task 2 - Implement Dataset Allocation
**Goal**: Ensure the mainframe has a place to store our manipulated data.

1.  Find the `ensure_dataset_exists` function (around line 72).
2.  Implement the logic to check and create the dataset:
    ```python
    response = datasets.list(dsname)
    if not any(item.dsname.upper() == dsname.upper() for item in response.items):
        options = DatasetOption(
            dsorg="PS", recfm="FB", lrecl=lrecl, 
            blksize=7161, primary=1, secondary=1, alcunit="TRK"
        )
        datasets.create(dsname, options=options)
    ```
**Why?** Unlike modern file systems, mainframe datasets must be "allocated" with specific attributes (like LRECL - Logical Record Length) before they can be written to.

### Step 5: Task 3 - Implement List Datasets Route
**Goal**: Create an API endpoint to verify our connection.

1.  Find the `handle_list_datasets` function (around line 85).
2.  Implement the logic to list datasets:
    ```python
    datasets = Datasets(profile)
    response = datasets.list(f"{hlq}.*")
    names = [item.dsname for item in response.items]
    return jsonify({"status": "success", "datasets": names})
    ```
**Why?** This teaches us how to wrap a Zowe SDK call into a Flask web route, making mainframe data accessible via a simple HTTP request.

### Step 6: Task 4 - Implement Main Manipulation Route
**Goal**: The core workflow—Download -> Manipulate -> Upload.

1.  Find the `handle_manipulate` function (around line 105).
2.  Implement the logic to download, manipulate, and upload:
    ```python
    datasets = Datasets(profile)
    # Ensure output dataset exists with LRECL 93
    ensure_dataset_exists(datasets, output_ds, lrecl=93)

    datasets.perform_download(input_ds, temp_in)
    with open(temp_in, "r") as f:
        content = f.read()

    manipulated_content = manipulate_data(content)

    with open(temp_out, "w") as f:
        f.write(manipulated_content)
    datasets.perform_upload(temp_out, output_ds)
    ```
**Why?** This is the automation "magic." We pull sensitive data into memory, clean it using our logic from Step 3, and push the safe version back to a new dataset.

### Step 7: Task 5 - Implement Download Dataset Route
**Goal**: Expose the cleaned data to the outside world.

1.  Find the `handle_download_dataset` function (around line 143).
2.  Implement the logic to download and return raw content:
    ```python
    datasets = Datasets(profile)
    datasets.perform_download(input_ds, temp_in)
    with open(temp_in, "r") as f:
        content = f.read()
    return jsonify({"status": "success", "content": content})
    ```

---

## Phase 2: Client Implementation (`client.py`)

Now that our server is ready, we'll build the client to interact with it.

### Step 8: Task 6 - Implement Credential Helper
**Goal**: Securely handle mainframe authentication.

1.  Open `client.py`.
2.  Find the `create_payload` function (around line 10).
3.  Replace the code inside with:
    ```python
    username = os.getenv("MAINFRAME_USER") or input("Enter Username: ")
    password = os.getenv("MAINFRAME_PASSWORD") or getpass.getpass("Enter Password: ")
    host = os.getenv("MAINFRAME_HOST", "mainframe.example.com")
    port = int(os.getenv("MAINFRAME_PORT", 5010))
    reject_unauthorized = os.getenv("MAINFRAME_REJECT_UNAUTHORIZED", "false").lower() == "true"

    payload = {
        "username": username, "password": password, "host": host,
        "port": port, "reject_unauthorized": reject_unauthorized
    }
    if extra_data:
        payload.update(extra_data)
    return payload
    ```

### Step 9: Task 7 - Implement Main Execution Logic
**Goal**: Use our client to trigger the server-side tasks.

1.  Find the `main` function (around line 36) in `client.py`.
2.  Implement the following tasks:

    **Task 1: List Datasets**
    ```python
    hlq = os.getenv("MAINFRAME_USER") or input("Enter HLQ to list: ")
    list_payload = create_payload({"hlq": hlq})
    list_response = requests.post("http://localhost:5010/list-datasets", json=list_payload)
    print("Found datasets:", list_response.json().get("datasets", []))
    ```

    **Task 2: Manipulate Data**
    ```python
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    response = requests.post("http://localhost:5010/manipulate", json=manipulate_payload)
    print(response.json().get("message", "Manipulation complete!"))
    ```

    **Task 3: Download and Display JSON**
    ```python
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
    ```

---

## Step 10: Run the Workshop! (8 minutes)

1.  **Start the Service**:
    In your terminal, run:
    ```bash
    python manipulator_service.py
    ```
    You should see "Running on http://0.0.0.0:5010". **Leave this terminal running.**

2.  **Run the Client**:
    Open a **second terminal** window, navigate back to the `scaffold/` folder, and run:
    ```bash
    python client.py
    ```

3.  **Verify the Result**:
    - The client should output "Success!".
    - Review the JSON output; the SSN data should be completely removed.

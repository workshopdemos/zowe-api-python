# Workshop: Mainframe Data Manipulation with Python

Welcome! In this workshop, you will build a Python service that connects to a mainframe, downloads a dataset, removes Social Security Numbers (SSN) entirely, and uploads the "clean" data back.

**No Python experience? No problem!** Just follow these steps. You can type the code or copy and paste it.

---

## Step 1: Install the Tools (5 minutes)

First, we need to install the Python libraries that do the heavy lifting.

1.  Open your terminal.
2.  Navigate to this `scaffold/` folder.
3.  Run this command:
    ```bash
    pip install -r requirements.txt
    ```

---

## Step 2: Set Your Credentials (2 minutes)

We need to tell the code how to log in to your mainframe.

1.  Find the file named `.env.example`.
2.  Rename it to exactly `.env`.
3.  Open `.env` and replace `your_username` and `your_password` with your real mainframe credentials.
4.  Save the file.

---

## Step 3: Task 1 - List Your Datasets (5 minutes)

Before we manipulate data, let's verify our connection by listing datasets under your username (HLQ).

1.  Open `manipulator_service.py`.
2.  Find the `handle_list_datasets` function (around line 84).
3.  Implement the logic to list datasets:
    ```python
    datasets = Datasets(profile)
    response = datasets.list(f"{hlq}.*")
    names = [item.dsname for item in response.items]
    return jsonify({"status": "success", "datasets": names})
    ```
4.  Open `client.py`.
5.  Find the `create_payload` function. This is a helper to avoid typing your password for every call. Replace the code inside with:
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
6.  Find the `TODO: Task 1` section in the `main` function. Add the code to call the new endpoint:
    ```python
    list_payload = create_payload({"hlq": os.getenv("MAINFRAME_USER", "ZOWEUSER")})
    list_response = requests.post("http://localhost:5010/list-datasets", json=list_payload)
    print("Found datasets:", list_response.json().get("datasets", []))
    ```

---

## Step 4: Implement Dataset Creation Logic (5 minutes)

Mainframe datasets must be "allocated" before they can be used. Let's add a check to create the output dataset if it doesn't exist.

1.  Open `manipulator_service.py`.
2.  Find the `ensure_dataset_exists` function (around line 32).
3.  Implement the logic to check and create:
    ```python
    response = datasets.list(dsname)
    if not any(item.dsname.upper() == dsname.upper() for item in response.items):
        options = DatasetOption(
            dsorg="PS", recfm="FB", lrecl=lrecl, 
            blksize=7161, primary=1, secondary=1, alcunit="TRK"
        )
        datasets.create(dsname, options=options)
    ```

---

## Step 5: Implement the Manipulation Logic (5 minutes)

Now that we can list datasets and ensure they exist, let's implement the logic to remove the SSN.

1.  Open `manipulator_service.py`.
2.  Find the `manipulate_data` function (around line 46).
3.  Look for the `TODO` comments inside the `for` loop.
4.  Replace the line for `rest` and the `new_line` reconstruction with this code:

```python
        # Remove SSN (chars 12-22) by skipping them
        rest = line[23:93]
        
        # Reconstruct the fixed-width line without SSN
        new_line = f"{account}{bill}{rest}"
```

5.  **Test it!** You can't run the full service yet, but you've just defined the "brain" of the operation.

---

## Step 6: Connect to the Mainframe (5 minutes)

Still in `manipulator_service.py`, scroll down to the `handle_manipulate` function (around line 101).

1.  Find **Step 1** (Ensure output dataset exists). Add this code:
    ```python
    # Ensure output dataset exists with LRECL 82 (since SSN is removed)
    ensure_dataset_exists(datasets, output_ds, lrecl=82)
    ```

2.  Find **Step 2** (Download the dataset). Add this code:
    ```python
    datasets.perform_download(input_ds, temp_in)
    with open(temp_in, "r") as f:
        content = f.read()
    ```

3.  Find **Step 3** (Upload the data). Add this code:
    ```python
    with open(temp_out, "w") as f:
        f.write(manipulated_content)
    datasets.perform_upload(temp_out, output_ds)
    ```

4.  **Save `manipulator_service.py`.**

---

## Step 7: Complete the Client (5 minutes)

Go back to `client.py`. We need to wire up the final manipulation call.

1.  Find the `TODO: Task 2` section. Add the code to call the manipulation endpoint:
    ```python
    manipulate_payload = create_payload({
        "input_dataset": input_ds,
        "output_dataset": output_ds
    })
    response = requests.post("http://localhost:5010/manipulate", json=manipulate_payload)
    print(response.json().get("message", "Manipulation complete!"))
    ```

2.  **Save `client.py`.**

---

## Step 8: Task 3 - Download and Display as JSON (5 minutes)

Finally, let's verify our work by downloading the manipulated dataset and displaying it in a modern JSON format.

1.  Open `manipulator_service.py`.
2.  Find the `handle_download_dataset` function (around line 143).
3.  Implement the logic to download and return raw content:
    ```python
    datasets = Datasets(profile)
    datasets.perform_download(input_ds, temp_in)
    with open(temp_in, "r") as f:
        content = f.read()
    return jsonify({"status": "success", "content": content})
    ```
4.  Open `client.py`.
5.  Find the `TODO: Task 3` section.
6.  Add the code to call the download endpoint and format the output:
    ```python
    download_payload = create_payload({"input_dataset": output_ds})
    download_response = requests.post("http://localhost:5010/download-dataset", json=download_payload)
    content = download_response.json().get("content", "")
    
    # Convert fixed-width text to a list of JSON objects
    records = []
    for line in content.splitlines():
        if len(line) >= 82:
            records.append({
                "account": line[0:8].strip(), "bill": line[8:12].strip(),
                "name": line[12:42].strip(), "phone": line[42:52].strip(),
                "email": line[52:82].strip()
            })
    print(json.dumps(records, indent=2))
    ```

---

## Step 9: Run the Workshop! (8 minutes)

Now we put it all together.

1.  **Start the Service**:
    In your terminal, run:
    ```bash
    python manipulator_service.py
    ```
    You should see "Running on http://0.0.0.0:5010". **Leave this terminal running.**

2.  **Run the Client**:
    Open a **second terminal** window, navigate back to this `scaffold/` folder, and run:
    ```bash
    python client.py
    ```
    If you didn't set up the `.env` file, it will ask for your username and password.

3.  **Verify the Result**:
    The client should say "Success!". Now, log in to your mainframe and check the `ZOWEUSER.PUBLIC.MANIPULATED.DATA` dataset. The SSNs should be gone, and each record should now be 82 characters long instead of 93!

---

## Bonus: Test Without Uploading

If you want to see the results in your terminal without changing the mainframe data:
1.  In `client.py`, change the URL for Task 3 to point to your input dataset:
    `download_payload = create_payload({"input_dataset": input_ds})`
2.  Run `python client.py` again. Note that the JSON parsing will fail because the input dataset still has the SSN (93 chars), while the client expects 82! This shows why the manipulation step is so important.

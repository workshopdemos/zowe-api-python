# Workshop: Mainframe Data Manipulation with Python

Welcome! In this workshop, you will build a Python service that connects to a mainframe, downloads a dataset, removes Social Security Numbers (SSN), and uploads the "clean" data back.

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

## Step 3: Implement the Manipulation Logic (5 minutes)

Open `manipulator_service.py`. We need to tell Python how to find the SSN in the COBOL data and remove it.

1.  Find the `manipulate_data` function (around line 34).
2.  Look for the `TODO` comments inside the `for` loop.
3.  Replace the line for `ssn` with this code:

```python
        # Remove SSN (chars 12-22) by replacing with 11 spaces
        ssn = " " * 11
```

4.  **Test it!** You can't run the full service yet, but you've just defined the "brain" of the operation.

---

## Step 4: Connect to the Mainframe (5 minutes)

Still in `manipulator_service.py`, scroll down to the `handle_manipulate` function (around line 75).

1.  Find **Step 1** (Use the helper to get the profile). Replace `profile = None` with:
    ```python
    profile = get_profile_from_request(data)
    ```

2.  Find **Step 2** (Download the dataset). Replace `content = ""` with:
    ```python
    datasets = Datasets(profile)
    datasets.perform_download(input_ds, "temp_in.txt")
    with open("temp_in.txt", "r") as f:
        content = f.read()
    ```

3.  Find **Step 3** (Upload the data). Add this code below the comment:
    ```python
    with open("temp_out.txt", "w") as f:
        f.write(manipulated_content)
    datasets.perform_upload("temp_out.txt", output_ds)
    ```

4.  **Save `manipulator_service.py`.**

---

## Step 5: Complete the Client (5 minutes)

Now open `client.py`. This is the "remote control" that tells the service what to do.

1.  Find the `main` function.
2.  Look for the `TODO` to send the request. Replace `response = None` with:
    ```python
    response = requests.post("http://localhost:5000/manipulate", json=payload)
    ```

3.  **Save `client.py`.**

---

## Step 6: Run the Workshop! (8 minutes)

Now we put it all together.

1.  **Start the Service**:
    In your terminal, run:
    ```bash
    python manipulator_service.py
    ```
    You should see "Running on http://0.0.0.0:5000". **Leave this terminal running.**

2.  **Run the Client**:
    Open a **second terminal** window, navigate back to this `scaffold/` folder, and run:
    ```bash
    python client.py
    ```
    If you didn't set up the `.env` file, it will ask for your username and password.

3.  **Verify the Result**:
    The client should say "Success!". Now, log in to your mainframe and check the `ZOWEUSER.PUBLIC.MANIPULATED.DATA` dataset. The SSNs should be replaced by spaces, but the names and emails should be exactly the same!

---

## Bonus: Test Without Uploading

If you want to see the results in your terminal without changing the mainframe data:
1.  In `client.py`, change the URL to:
    `"http://localhost:5000/manipulate-download"`
2.  Run `python client.py` again. The manipulated data will print right in your terminal!

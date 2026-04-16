# Building a Standalone Zowe Python Client

This guide explains how to use the Zowe Python SDK to connect directly to a mainframe and list files (datasets). It's designed for someone who is completely new to Python and to see how to connect to the SDK.

---

## Understanding the Code

We will be using `simple_zowe_client.py`.

If you've never used Python or a "Software Development Kit" (SDK) before, here's what the script is doing:

- **`from zowe.zos_files_for_zowe_sdk import Datasets`**: Think of this as pulling a specialized tool out of a toolbox. The "Zowe SDK" is the toolbox, and `Datasets` is the tool specifically designed for handling mainframe files.
- **`profile = { ... }`**: This is a "dictionary" in Python. It's a way of grouping together related information. Here, it stores the mainframe's address (`host`), the "doorway" we use to enter (`port`), and your secret keys (`username` and `password`).
- **`rejectUnauthorized: False`**: Mainframes often use internal security certificates that your computer might not recognize. Setting this to `False` tells Python, "I trust this connection; don't block it even if the certificate looks unfamiliar."
- **`if __name__ == "__main__":`**: This tells Python to only run the test code at the bottom of the file if you execute this script directly. If you used this file inside a bigger project later, this test part would be ignored. It calls `list_mainframe_datasets` and then prints the output it receives.
- **`list_mainframe_datasets`**: This is the code block we need to create.

---

## Implementing the Connection Logic

In `simple_zowe_client.py`, there's a `TODO 1` marker. To make the script functional, you must replace the `pass` on Line 18 with the following code:

**Action**: Replace the `pass` on Line 18 in `simple_zowe_client.py` with this code:

```python
    try:
        # Step A: Initialize the Zowe SDK's dataset tool with our connection details
        datasets_service = Datasets(profile)
        
        # Step B: Ask the mainframe to list all files starting with our HLQ
        # The wildcard (.*) means "find everything that starts with this name"
        response = datasets_service.list(f"{hlq}.*")
        
        # Step C: Extract just the names of the files from the results and return them
        return [item.dsname for item in response.items]
        
    except Exception as e:
        # If anything goes wrong (wrong password, bad connection), print the error
        print(f"An error occurred while connecting to z/OSMF: {str(e)}")
        return None
```

---

## Updating Connection Information

In order to connect successfully, we must add user connection information. For simplicity, we are hardcoding the values in this script. **Note**: This is not a good programming practice for real code, but serves well for this workshop.

In `__main__`, update the following values:

- **Action**: Replace `YOUR_USERNAME`, `YOUR_PASSWORD`, and `YOUR_HLQ` with **CUST001**.

---

## Executing the Program

Once you have added the code in the previous steps and saved the file, you can run it from your terminal.

**Action**:
1. Open your terminal using the hamburger menu (**Terminal** > **New Terminal**).
2. Type the following command:
   ```bash
   python simple_zowe_client.py
   ```

**Expected Result**:
If your credentials and connection settings are correct, you will see a list of datasets printed out like this:

```text
Connecting to 10.1.2.123:10443...
Successfully retrieved 5 datasets:
 - CUST001.DATA1
 - CUST001.DATA2
 ...
```

---

## Next Steps

Once you've completed this, let's create a service that does this and more. See **apiml_service_app_readme.md** for the next steps.

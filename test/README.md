# Standalone Direct Manipulator

This client performs the mainframe operations directly using the Zowe Python SDK, without requiring the Flask service to be running.

## Setup

1.  Navigate to the `test/` directory.
2.  Install dependencies:
    ```bash
    pip install zowe-python-sdk-bundle python-dotenv
    ```
3.  Configure your `.env` file (you can copy it from the `scaffold` or `solution` folder).

## Running

Run the manipulator directly:
```bash
python direct_manipulator.py
```

The manipulator will:
1.  Connect to the mainframe using the credentials in your `.env` file or by prompting you.
2.  Download the input dataset.
3.  Remove the SSNs in memory (replacing them with spaces).
4.  Upload the results to the output dataset.

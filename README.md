# FDN04-Python: Mainframe Data Manipulation Workshop

Welcome to the **Mainframe Data Manipulation** workshop! This project demonstrates how to use Python to simplify interactions with the mainframe and automate complex tasks like data manipulation.

## Why Python for Mainframe?

Interacting with the mainframe traditionally requires specialized knowledge of tools like TSO/ISPF or JCL. By using Python and the **Zowe Python SDK**, we can:
- **Simplify Mainframe Access**: Use standard REST APIs (z/OSMF) to interact with datasets, jobs, and consoles.
- **Automate Workflows**: Easily integrate mainframe data into modern CI/CD pipelines or data processing services.
- **Leverage Modern Libraries**: Use powerful Python libraries like `Flask` for creating web services.

In this workshop, we build a service that downloads sensitive fixed-width COBOL data from a mainframe dataset, removes Social Security Numbers (SSN) while preserving the rest of the record structure, and uploads the "clean" version back—all through a simple REST API.

---

## Data Format (COBOL Copybook Style)

The service expects data in a fixed-width format (93 characters per record):
- **Account Number**: 8 characters
- **Current Bill**: 4 characters
- **Social Security Number**: 11 characters
- **Name**: 30 characters
- **Phone**: 10 characters
- **Email**: 30 characters

---

## Understanding the Imports

Here is a breakdown of the key libraries used in this project and why they are essential:

### 1. `zowe.zos_files_for_zowe_sdk`
- **What it is**: Part of the Zowe Python SDK.
- **How it's used**: 
    - `Datasets`: Provides methods like `perform_download` and `perform_upload` to read and write mainframe datasets using temporary local files.
- **Benefit**: No need to write complex JCL or use FTP; it's all handled through clean Python methods.

### 2. `flask`
- **What it is**: A lightweight web framework for Python.
- **How it's used**: It turns our Python script into a REST API service. The `@app.route('/manipulate', methods=['POST'])` decorator defines an endpoint that our client can call.
- **Benefit**: Allows the mainframe manipulation logic to be triggered by any application that can send an HTTP request.

### 3. `requests`
- **What it is**: The standard Python library for making HTTP requests.
- **How it's used**: Used in the `client.py` application to send the mainframe credentials and dataset names to our Flask service.
- **Benefit**: Simplifies the process of communicating between the client and the service.

### 4. `python-dotenv`
- **What it is**: A library that reads key-value pairs from a `.env` file and sets them as environment variables.
- **How it's used**: Allows participants to store their mainframe credentials securely in a `.env` file rather than hardcoding them or typing them every time.
- **Benefit**: Improves security and developer experience.

---

## Project Structure

- `scaffold/`: The "hands-on" part of the workshop with TODOs for you to complete.
- `solution/`: The fully implemented version for reference or troubleshooting.
- `test/`: A standalone client that performs the manipulation directly on the mainframe.

## Getting Started

1.  Navigate to the `scaffold/` directory.
2.  Follow the instructions in `scaffold/README.md`.

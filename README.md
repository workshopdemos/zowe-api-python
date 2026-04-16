# FDN04-Python: Python and Zowe API Mediation Layer Hands On Workshop

Welcome to the **Python and API Mediation Layer** workshop! This project demonstrates how to use Python to work with Zowe API and create a Zowe API Mediation Layer plugin.

The example implementation is simplistic:
- List Datasets
- Download a Dataset
- Read a Dataset, make changes and write it to a new dataset name

Listing and Downloading datasets are basic functions of z/OSMF.  These are included just to illustrate how existing functions can be mapped into Python Libraries.  

The modification of datasets illustrates how different functions can be combined into a single API call.  This could be written as a library and shared with Python developers, but that would exclude any other application from benefitting from the same code. It also means maintaining a library and ensuring it gets distributed.  And potentially different versions of the code for different programming languages.

Using an API Mediation Layer plugin to perform work can solve many problems:
- The code is centrally managed.
- It is language agnostic. 
    - The API can be written in Python but the calling apps can be in another language.
- It provides a Swagger Interface.
- Can be mainframe hosted

While the example is pretty simple, to make it easy to understand, the primary purpose of the workshop is to illustrate accessing Zowe's SDK and implementing a Zowe API ML Plugin using Python.

## Why Python for Mainframe?

Interacting with the mainframe traditionally requires specialized knowledge of tools like TSO/ISPF or JCL. By using Python and the **Zowe Python SDK**, we can:
- **Simplify Mainframe Access**: Use standard REST APIs (z/OSMF) to interact with datasets, jobs, and consoles.
- **Automate Workflows**: Easily integrate mainframe data into modern CI/CD pipelines or data processing services.
- **Leverage Modern Libraries**: Use powerful Python libraries like `FastAPI` for creating web services.

In this workshop, we build a service that downloads sensitive fixed-width COBOL data from a mainframe dataset, removes Social Security Numbers (SSN) entirely while preserving the rest of the record structure, and uploads the "clean" version back—all through a simple REST API.  This is not intended to be a replacement for tools creating test data, but just a simple example to illustrate some data manipulation.

---

## Data Format

The **input** service expects data in a fixed-width format (93 characters per record):
- **Account Number**: 8 characters
- **Current Bill**: 4 characters
- **Social Security Number**: 11 characters
- **Name**: 30 characters
- **Phone**: 10 characters
- **Email**: 30 characters

The **output** will be a fixed-width format (82 characters per record) with the SSN removed.

---

## Understanding the Imports

Here is a breakdown of the key libraries used in this project and why they are essential:

### 1. `zowe.zos_files_for_zowe_sdk`
- **What it is**: Part of the Zowe Python SDK.
- **How it's used**: 
    - `Datasets`: Provides methods like `perform_download` and `perform_upload` to read and write mainframe datasets using temporary local files.
- **Benefit**: No need to write complex JCL or use FTP; it's all handled through clean Python methods.

### 2. `fastapi`
- **What it is**: A lightweight web framework for Python.
- **How it's used**: It turns our Python script into a REST API service. The `@app.post("/manipulate")` decorator defines an endpoint that our client can call.
- **Benefit**: Allows the mainframe manipulation logic to be triggered by any application that can send an HTTP request.

### 3. `python-dotenv`
- **What it is**: A library that reads key-value pairs from a `.env` file and sets them as environment variables.
- **How it's used**: Allows participants to store their mainframe credentials securely in a `.env` file rather than hardcoding them or typing them every time.
- **Benefit**: Improves security and developer experience.

## Python Conventions

Python uses **indentation** to define logic blocks. Everything in the same block must be at the same indentation level. If you are copying and pasting code, ensure the indentation remains consistent. You can use the **TAB** key to indent blocks of code. Note that spaces and tabs should not be mixed; for this workshop, we will use standard 4-space indentation (or the TAB key).

### Key Concepts:
These are common things in Python. If you are unfamiliar with these, this will help you understand Python a little better.

#### Imports
```python
from zowe.zos_files_for_zowe_sdk import Datasets, DatasetOption
import logging
import os
```
- These lines import external libraries into the application for use.

#### Functions
```python
def name(parameter):
    # Code goes here
```
- This defines a function. All code belonging to the function must be indented (usually 1 TAB or 4 spaces).

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
@app.post("/manipulate")
```
- Decorators modify the behavior of the function immediately following them.
- In FastAPI, decorators like `@app.post` map a URL (endpoint) to a specific Python function.

---

## Project Structure

- `./`: Current working folder with files to be worked on.
- `completed_files/`: The fully implemented version for reference or troubleshooting.
- `config/`: Configuration files for the services and the API ML.
- `simple_zowe_client.py`: Starting point, connecting to Zowe API through Python.
- `simple_zowe_client_readme.md`: Instructions for the simple client.
- `apiml_service_app.py`: Starting point for the Python API ML Service.
- `apiml_service_app_readme.md`: Instructions for the apiml_service_app.
- `apiml_service_app_additional_info.md`: A detailed explanation of the application.
- `pythonSwagger.json`: A Swagger interface for the APIML.
- `start_apiml_service.sh`: Starts the API ML layer.

---
## Getting Started

1. **Start with `simple_zowe_client_readme.md`**
   - Create a simple Zowe connection to the base Dataset API. It does not use APIML.
   - This is used as an introduction to accessing Zowe from Python.

2. **Start the API Mediation Layer**
   - The API Mediation Layer needs to be running.
   - We will register our service with it.

3. **Proceed to `apiml_service_app_readme.md`**
   - Create the APIML endpoint.
   - Start the Service.
   - Test it stand-alone and within the API ML.

4. **Complete with `apiml_client_readme.md`**
   - Create a client to interact with the API ML service.

5. **Addition Review**
   - `apiml_service_app_additional_info.md` contains more infomration and reference materials.
   

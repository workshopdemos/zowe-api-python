# Service Application Details: `apiml_service_app.py`

This document provides a detailed breakdown of the `apiml_service_app.py` script, which implements a FastAPI-based microservice designed to interact with IBM z/OS mainframe datasets using the Zowe SDK and integrate with the Zowe API Mediation Layer (ML).

---

## Imports and Initial Configuration
**Lines 1-18**
- **Purpose**: Loads all necessary Python libraries and sets up the environment.
- **Key Modules**:
    - `fastapi`: The web framework used to build the API.
    - `uvicorn`: The ASGI server that runs the FastAPI application.
    - `pydantic`: Used for data validation and settings management via Python type annotations.
    - `zowe.zos_files_for_zowe_sdk`: Part of the Zowe Python SDK, used for mainframe dataset operations (list, download, upload, create).
    - `zowe_apiml_onboarding_enabler_python`: A library for registering the service with the Zowe API Mediation Layer.
- **Configuration**: Sets up logging and determines the absolute path to the `config/service-configuration.yml` file.

---

## API ML Enabler and SSL Setup
**Lines 19-29**
- **Purpose**: Initializes the connection to the Zowe API Mediation Layer and prepares for secure communication.
- **`enabler = PythonEnabler(...)`**: Loads the service configuration and prepares the "onboarding" logic.
- **SSL Configuration**: Retrieves certificate and key paths from the enabler configuration. These are used later to start the server over HTTPS.

---

## FastAPI Instance
**Line 30**
- **Purpose**: Initializes the core `app` object with metadata (title and description). This object manages all routes and middleware.

---

## Data Models (Pydantic)
**Lines 34-49**
- **Purpose**: Defines the structure of expected JSON payloads for incoming POST requests.
- **`ZoweProfile`**: The base model containing mainframe connection details (username, password, host, port).
- **`ListDatasetsRequest`**: Extends the profile to include a High-Level Qualifier (`hlq`) for searching datasets.
- **`ManipulateRequest`**: Extends the profile to specify `input_dataset` and `output_dataset` for data transformation.
- **`DownloadRequest`**: Extends the profile to specify which dataset to retrieve.

---

## Helper Functions
**Lines 50-85**
- **`get_profile(data)`**: A utility that converts the Pydantic request data into a dictionary format required by the Zowe SDK's `Datasets` class.
- **`manipulate_data(content)`**: The "Business Logic" of the service. It iterates through lines of COBOL fixed-width data, identifies specific character positions (offsets), and reconstructs the lines while **removing Social Security Numbers (SSNs)** from characters 12-22.
- **`ensure_dataset_exists(...)`**: Checks if the target output dataset exists on the mainframe. If not, it programmatically allocates it with specific parameters (LRECL, RECFM, etc.) using the Zowe SDK.

---

## Mainframe Operation Routes (POST)
**Lines 86-137**
- **`/list-datasets`**: Lists all datasets matching a pattern (e.g., `USER.TEST.*`).
- **`/manipulate`**: 
    1. Connects to the mainframe.
    2. Ensures the destination dataset is allocated.
    3. Downloads the input dataset to a local temporary file.
    4. Reads the file, applies the `manipulate_data` logic.
    5. Writes the result to another temporary file and uploads it back to the mainframe.
    6. Cleans up local temporary files.
- **`/download-dataset`**: Downloads a dataset and returns its raw content as a string in the JSON response.

---

## API ML Management Routes (GET)
**Lines 138-149**
- **`/registerInfo`**: A manual trigger to re-register the service with the API ML Discovery Service.
- **`/unregisterInfo`**: A manual trigger to remove the service from the Discovery Service.

---

## Informational and Utility Routes (GET)
**Lines 150-181**
- **`/hello`**: A simple diagnostic endpoint to confirm the service is responding.
- **`/apidoc`**: Reads `pythonSwagger.json` from the disk and serves it as a JSON response. This is used by the API Mediation Layer to display the API's documentation.
- **`/application/info`**: Provides metadata about the build (version, OS, build time).
- **`/application/health`**: Returns `{"status": "UP"}`, used by external monitors or the API ML to check if the service is healthy.

---

## Main Execution Block
**Lines 182-192**
- **Purpose**: The entry point for starting the script.
- **Registration**: Automatically calls `enabler.register()` on startup.
- **`uvicorn.run(...)`**: Starts the web server. It checks for the existence of SSL certificates; if found, it starts on port `10018` using HTTPS; otherwise, it falls back to HTTP and logs a warning.

---

## Simple Profile
This is a simplified Profile model for Zowe API ML.  In a real implementation, the application would use Zowe's `ProfileManager` to manage the Zowe profiles.  

---
## Library Documentation and Resources

For more information on the libraries used in this project, please refer to their official documentation:

- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/) - The modern, fast (high-performance), web framework for building APIs with Python.
- **Uvicorn**: [https://www.uvicorn.org/](https://www.uvicorn.org/) - The lightning-fast ASGI server implementation used to run the FastAPI application.
- **Pydantic**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/) - Data validation and settings management using Python type annotations.
- **Zowe Python SDK**: [https://github.com/zowe/zowe-python-sdk](https://github.com/zowe/zowe-python-sdk) - The SDK used to interact with mainframe services via Python.
- **Zowe API Mediation Layer**: [https://docs.zowe.org/stable/extend/extend-apiml/onboard-overview/](https://docs.zowe.org/stable/extend/extend-apiml/onboard-overview/) - Documentation for onboarding services to the API Mediation Layer.
- **IBM z/OS Datasets**: [IBM Documentation](https://www.ibm.com/docs/en/zos) - General information on z/OS datasets and their properties (LRECL, RECFM, etc.).

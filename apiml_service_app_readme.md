# Implementing the Mainframe Data Manipulator Service

This service provides an API for mainframe data manipulation and registers itself with the Zowe API Mediation Layer (ML).

---

## Serving the API

Python provides several libraries to assist in creating the API. The most important are:

- **`fastapi`**: Provides the API library to serve the web routes.
- **`uvicorn`**: A high-performance ASGI web server.
- **`logging`**: Used for troubleshooting and monitoring.
- **`zowe`**: Specifically the Zowe Python SDK for mainframe dataset operations.
- **`zowe_apiml_onboarding_enabler_python`**: Simplifies onboarding to the Zowe API ML.

---

## Onboarding

We use the `PythonEnabler` to handle registration with the Zowe API ML. This relies on `config/service-configuration.yml` for connection and metadata details.

The following diagnostic endpoints are available:

- **`register_python_enabler()`**: Manually register the service.
- **`unregister_python_enabler()`**: Manually unregister the service.
- **`hello()`**: Quickly test the API's responsiveness.
- **`get_swagger()`**: Serve the Swagger API documentation.
- **`get_application_info()`**: Basic application metadata.
- **`get_application_health()`**: Health status indicator.

---

## API Endpoints

We are serving three primary API endpoints:

- **`/manipulate`**: Expects a source and target dataset. Removes sensitive data (SSNs) before creating/updating the target.
- **`/list-datasets`**: Lists datasets based on a High-Level Qualifier (HLQ).
- **`/download-dataset`**: Downloads a dataset and returns its content in JSON format.

---

## Task 1: Clean Sensitive Data

**Location**: `def manipulate_data(content: str) -> str:` (Line 62)

This function iterates through every line in a file and removes Social Security Numbers (SSNs).

**Action**: Replace the `pass` on Line 70 in `apiml_service_app.py` with this code:

```python
        # Make sure every line is 93 characters long (adds spaces if needed)
        line = f"{line:<93}"
            
        # Slicing: Grab specific characters from the line
        account = line[0:8]   # Characters 0 to 7
        bill = line[8:12]     # Characters 8 to 11
        
        # Skip characters 12-22 (the SSN) and grab everything from 23 onwards
        rest = line[23:93]
        
        # Combine the clean parts back together
        new_line = f"{account}{bill}{rest}"
        manipulated_lines.append(new_line)
```

**Action**: Replace `return ""` on Line 73 with this code:

```python
    # Combine all the clean lines back into one big block of text
    return "\n".join(manipulated_lines)
```

---

## Task 2: Manage Mainframe Files

**Location**: `def ensure_dataset_exists(...)` (Line 75)

This helper ensures a file exists on the mainframe before writing to it.

**Action**: Replace the `pass` on Line 81 in `apiml_service_app.py` with this code:

```python
        # List files matching the name we want
        response = datasets.list(dsname)
        
        # If the file is NOT found in the list, create it
        if not any(item.dsname.upper() == dsname.upper() for item in response.items):
            # Define the file settings (size, format, etc.)
            options = DatasetOption(
                dsorg="PS", recfm="FB", lrecl=lrecl, 
                blksize=7161, primary=1, secondary=1, alcunit="TRK"
            )
            # Create the file on the mainframe
            datasets.create(dsname, options=options)
```

---

## Task 3: Search for Files

**Location**: `async def handle_list_datasets(...)` (Line 87)

**Action**: Replace the `TODO 4` comment on Line 93 in `apiml_service_app.py` with this code:

```python
    profile = get_profile(request) # Convert credentials to a Zowe profile
    try:
        datasets = Datasets(profile) # Connect to the mainframe
        # Search for files starting with the user's High-Level Qualifier (HLQ)
        response = datasets.list(f"{request.hlq}.*")
        
        # Extract just the file names from the results
        names = [item.dsname for item in response.items]
        return {"status": "success", "datasets": names}
    except Exception as e:
        logger.error(f"Error listing datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Task 4: Transform the Data

**Location**: `async def handle_manipulate(...)` (Line 96)

**Action**: Replace the `TODO 5` comment on Line 105 in `apiml_service_app.py` with this code:

```python
    try:
        datasets = Datasets(profile)
        ensure_dataset_exists(datasets, request.output_dataset, lrecl=93)

        # 2. Download the mainframe file to your local computer
        datasets.perform_download(request.input_dataset, temp_in)
        
        # 3. Open and read the downloaded file
        with open(temp_in, "r") as f:
            content = f.read()

        # 4. Clean the data using our function from Task 1
        manipulated_content = manipulate_data(content)

        # 5. Save the cleaned data to a new local file
        with open(temp_out, "w") as f:
            f.write(manipulated_content)
            
        # 6. Upload the cleaned file back to the mainframe
        datasets.perform_upload(temp_out, request.output_dataset)
        
        return {"status": "success", "message": "Data manipulated and uploaded"}
```

**Action**: Replace the `pass` on Line 113 with this code:

```python
        # Delete the temporary files from your local computer
        if os.path.exists(temp_in): os.remove(temp_in)
        if os.path.exists(temp_out): os.remove(temp_out)
```

---

## Starting the Services

**Action**:
1. Open a terminal and start the API ML background service:
   ```bash
   ./start_apiml_service.sh
   ```
2. Open a **New Terminal** and start the Python service:
   ```bash
   python apiml_service_app.py
   ```

**Expected Result**:
You should see logging indicating a successful registration with Eureka:
```text
INFO:zowe_apiml_onboarding_enabler_python.registration:Service registered successfully.
INFO:     Uvicorn running on https://0.0.0.0:10018 (Press CTRL+C to quit)
```

---

## Testing the API Call

You can test the direct API call to verify the service is running correctly.

**Action**:
1. Open a **New Terminal**.
2. Run the following command:
   ```bash
   http --verify=./localhost/localca.cer GET https://localhost:10018/pythonservice/hello
   ```

**Expected Result**:
```json
{
    "message": "Hello world in swagger"
}
```

---

## Testing via the API Gateway

Once the service is registered, you can access it through the Zowe API Gateway (Port 10010).

**Action**:
Run the following command:
```bash
http --verify=./localhost/localca.cer GET https://localhost:10010/pythonservice/api/v1/hello
```

---

## Next Steps

Once you've verified the service is running, proceed to create a client application to use the API. See **apiml_client_readme.md** for the next steps.

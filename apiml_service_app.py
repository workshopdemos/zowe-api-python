import os
import yaml
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from zowe.zos_files_for_zowe_sdk import Datasets
from zowe_apiml_onboarding_enabler_python.registration import PythonEnabler


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(base_directory, 'config/service-configuration.yml')

# Initialize API ML enabler
enabler = PythonEnabler(config_file=config_file_path)

# Load SSL configuration
ssl_config = enabler.ssl_config
cert_file = os.path.abspath(os.path.join(base_directory, ssl_config.get("certificate")))
key_file = os.path.abspath(os.path.join(base_directory, ssl_config.get("keystore")))

if not cert_file or not key_file:
    logger.warning("SSL certificate or key file is missing in service-configuration.yml. Falling back to default if necessary.")

app = FastAPI(title="Mainframe Data Manipulator Service", description="FastAPI implementation of Mainframe Data Manipulator Service")

base_url = '/pythonservice'

class ZoweProfile(BaseModel):
    username: str
    password: str
    host: str = '10.1.2.123'
    port: int = 10443

class ListDatasetsRequest(ZoweProfile):
    hlq: str

class ManipulateRequest(ZoweProfile):
    input_dataset: str
    output_dataset: str

class DownloadRequest(ZoweProfile):
    input_dataset: str

def get_profile(data: ZoweProfile):
    """
    Helper function to create a Zowe profile dictionary from a Pydantic model.
    """
    return {
        "host": data.host,
        "port": data.port,
        "user": data.username,
        "password": data.password,
        "rejectUnauthorized": False
    }

def manipulate_data(content: str) -> str:
    """
    Implement manipulation logic for fixed-width COBOL data.
    Goal: Remove Social Security Numbers entirely.
    """
    manipulated_lines = []
    for line in content.splitlines():
        # TODO 1: Implement line transformation logic here
        pass # REPLACE THIS LINE # REPLACE THIS LINE
    
    # TODO 2: Return the final joined string
    return ""

def ensure_dataset_exists(datasets: Datasets, dsname: str, lrecl: int = 93):
    """
    Helper to check if a dataset exists, and create it if not.
    """
    try:
        # TODO 3: Implement dataset existence check and creation logic here
        pass # REPLACE THIS LINE
    except Exception as e:
        logger.error(f"Error ensuring dataset {dsname} exists: {str(e)}")
        raise e

@app.post(f"{base_url}/list-datasets")
async def handle_list_datasets(request: ListDatasetsRequest):
    """
    Route to list datasets for a given HLQ.
    """
    print("made it here!")
    # TODO 4: Implement logic to list datasets using Zowe SDK
    return {"status": "success", "datasets": []}

@app.post(f"{base_url}/manipulate")
async def handle_manipulate(request: ManipulateRequest):
    """
    Main manipulation route.
    """
    profile = get_profile(request)
    temp_in = "temp_in.txt"
    temp_out = "temp_out.txt"

    try:
        # TODO 5: Implement the manipulation workflow (Download -> Transform -> Upload)
        return {"status": "success", "message": "Data manipulated and uploaded"}

    except Exception as e:
        logger.error(f"Error during manipulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # TODO 6: Implement local file cleanup logic
        pass # REPLACE THIS LINE

@app.post(f"{base_url}/download-dataset")
async def handle_download_dataset(request: DownloadRequest):
    """
    Route to download a dataset and return its content.
    """
    print("Made it here")
    profile = get_profile(request)
    temp_in = "temp_download.txt"

    try:
        datasets = Datasets(profile)
        datasets.perform_download(request.input_dataset, temp_in)
        with open(temp_in, "r") as f:
            content = f.read()
        return {"status": "success", "content": content}

    except Exception as e:
        logger.error(f"Error during download: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_in):
            os.remove(temp_in)

@app.get(f"{base_url}/registerInfo")
def register_python_enabler():
    """Test Endpoint to manually register the service."""
    enabler.register()
    return {"message": "Registered with Python eureka client to Discovery service"}

@app.get(f"{base_url}/unregisterInfo")
def unregister_python_enabler():
    """Test Endpoint to manually unregister the service."""
    enabler.unregister()
    return {"message": "Unregistered Python eureka client from Discovery service"}

@app.get(f"{base_url}/hello")
def hello():
    """Simple hello endpoint for testing."""
    return {"message": "Hello world in swagger"}

@app.get(f"{base_url}/apidoc")
def get_swagger():
    swagger_path = os.path.join(base_directory, 'pythonSwagger.json')
    try:
        with open(swagger_path) as f:
            data = yaml.safe_load(f)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Swagger file not found")

@app.get(f"{base_url}/application/info")
def get_application_info():
    return {
        "build": {
            "name": "manipulator-service",
            "operatingSystem": "Mac OS X",
            "time": 1660222556.497,
            "machine": "local",
            "number": "n/a",
            "version": "1.0.0",
        }
    }

@app.get(f"{base_url}/application/health")
def get_application_health():
    return {"status": "UP"}

if __name__ == "__main__":
    # Register with API ML
    enabler.register()
    
    # Run with SSL if certificates exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        uvicorn.run(app, host="0.0.0.0", port=10018, ssl_certfile=cert_file, ssl_keyfile=key_file)
    else:
        logger.warning("Starting without SSL as certificates were not found.")
        uvicorn.run(app, host="0.0.0.0", port=10018)

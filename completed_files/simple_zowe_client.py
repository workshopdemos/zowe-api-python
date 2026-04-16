from zowe.zos_files_for_zowe_sdk import Datasets

def list_mainframe_datasets(host, port, user, password, hlq):
    """
    Connects directly to the z/OSMF API using the Zowe Python SDK 
    to list datasets for a given High-Level Qualifier (HLQ).
    """
    # Define the connection profile for z/OSMF
    profile = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "rejectUnauthorized": False  # Set to False to bypass SSL certificate validation for internal/self-signed certs
    }
    
    try:
        # Initialize the Datasets class from the Zowe SDK
        datasets_service = Datasets(profile)
        
        # Call the list method to find datasets matching the pattern
        # The pattern uses the HLQ and a wildcard (.*) to find all matching datasets
        response = datasets_service.list(f"{hlq}.*")
        
        # Extract and return the names of the datasets found
        return [item.dsname for item in response.items]
        
    except Exception as e:
        print(f"An error occurred while connecting to z/OSMF: {str(e)}")
        return None

if __name__ == "__main__":
    # Example values (replace with actual mainframe details for testing)
    MAINFRAME_HOST = "10.1.2.123"
    MAINFRAME_PORT = 10443
    USERNAME = "CUST001"
    PASSWORD = "CUST001"
    HLQ = "CUST001"

    print(f"Connecting to {MAINFRAME_HOST}:{MAINFRAME_PORT}...")
    datasets = list_mainframe_datasets(MAINFRAME_HOST, MAINFRAME_PORT, USERNAME, PASSWORD, HLQ)
    
    if datasets is not None:
        print(f"Successfully retrieved {len(datasets)} datasets:")
        for ds in datasets:
            print(f" - {ds}")
    else:
        print("Failed to retrieve datasets. Check your connection settings.")
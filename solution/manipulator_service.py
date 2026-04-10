from flask import Flask, request, jsonify
from zowe.zos_files_for_zowe_sdk import Datasets, DatasetOption
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_profile_from_request(data):
    """
    Helper function to extract connection info and create a Zowe profile dictionary.
    """
    username = data.get('username')
    password = data.get('password')
    host = data.get('host', 'mainframe.example.com')
    port = data.get('port', 5010)
    reject_unauthorized = False

    if not username or not password:
        return None

    return {
        "host": host,
        "port": port,
        "user": username,
        "password": password,
        "rejectUnauthorized": False
    }

def ensure_dataset_exists(datasets, dsname, lrecl=93):
    """
    Checks if a dataset exists, and creates it if not.
    Attributes: Sequential, LRECL=lrecl, BLKSIZE=7161, RECFM=FB
    """
    try:
        # Check if dataset exists
        response = datasets.list(dsname)
        if not any(item.dsname.upper() == dsname.upper() for item in response.items):
            logging.info(f"Dataset {dsname} not found. Creating it...")
            # Create sequential dataset with specified attributes using DatasetOption
            options = DatasetOption(
                dsorg="PS",
                recfm="FB",
                lrecl=lrecl,
                blksize=7161,
                primary=1,
                secondary=1,
                alcunit="TRK"
            )
            datasets.create(dsname, options=options)
            logging.info(f"Dataset {dsname} created successfully.")
        else:
            logging.info(f"Dataset {dsname} already exists.")
    except Exception as e:
        logging.error(f"Error ensuring dataset {dsname} exists: {str(e)}")
        raise e

def manipulate_data(content):
    """
    Manipulation logic for fixed-width COBOL data.
    Goal: Remove Social Security Numbers entirely.
    Input: 93 chars, Output: 82 chars.
    """
    manipulated_lines = []
    for line in content.splitlines():
        # Ensure the line is padded to at least 93 chars to handle trailing spaces
        line = f"{line:<93}"
            
        account = line[0:8]
        bill = line[8:12]
        
        # Skip SSN (chars 12-22) and take the rest
        rest = line[23:93]
        
        new_line = f"{account}{bill}{rest}"
        manipulated_lines.append(new_line)
    
    return "\n".join(manipulated_lines)

@app.route('/list-datasets', methods=['POST'])
def handle_list_datasets():
    data = request.json
    hlq = data.get('hlq')
    profile = get_profile_from_request(data)

    if not profile or not hlq:
        return jsonify({"error": "Missing credentials or HLQ"}), 400

    try:
        datasets = Datasets(profile)
        response = datasets.list(f"{hlq}.*")
        names = [item.dsname for item in response.items]
        return jsonify({"status": "success", "datasets": names})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/manipulate', methods=['POST'])
def handle_manipulate():
    data = request.json
    input_ds = data.get('input_dataset')
    output_ds = data.get('output_dataset')

    profile = get_profile_from_request(data)

    if not profile or not input_ds or not output_ds:
        return jsonify({"error": "Missing required fields"}), 400

    temp_in = "temp_in.txt"
    temp_out = "temp_out.txt"

    try:
        datasets = Datasets(profile)
        
        # Ensure output dataset exists with LRECL 82 (since SSN is removed)
        ensure_dataset_exists(datasets, output_ds, lrecl=93)

        datasets.perform_download(input_ds, temp_in)
        
        with open(temp_in, "r") as f:
            content = f.read()

        manipulated_content = manipulate_data(content)

        with open(temp_out, "w") as f:
            f.write(manipulated_content)
            
        datasets.perform_upload(temp_out, output_ds)
        
        return jsonify({
            "status": "success",
            "message": f"Data manipulated and uploaded to {output_ds}"
        })

    except Exception as e:
        logging.error(f"Error during manipulation: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_in): os.remove(temp_in)
        if os.path.exists(temp_out): os.remove(temp_out)

@app.route('/download-dataset', methods=['POST'])
def handle_download_dataset():
    """
    Downloads a dataset and returns its raw content.
    """
    data = request.json
    input_ds = data.get('input_dataset')
    profile = get_profile_from_request(data)

    if not profile or not input_ds:
        return jsonify({"error": "Missing required fields"}), 400

    temp_in = "temp_download.txt"

    try:
        datasets = Datasets(profile)
        datasets.perform_download(input_ds, temp_in)
        
        with open(temp_in, "r") as f:
            content = f.read()
        print("c:", content)
        json_output = []
        for line in content.splitlines():
            print("line:", line)
            record = {
                "account": line[0:8].strip(),
                "bill": line[8:12].strip(),
                "name": line[12:42].strip(),
                "phone": line[42:52].strip(),
                "email": line[52:82].strip()
            }
            json_output.append(record)
        print("jsonout", json_output)
        return jsonify({
            "status": "success",
            "content": json_output
        })
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_in): os.remove(temp_in)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)

from flask import Flask, request, jsonify
from zowe.zos_files_for_zowe_sdk import Datasets
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
    reject_unauthorized = data.get('reject_unauthorized', False)

    if not username or not password:
        return None

    return {
        "host": host,
        "port": port,
        "user": username,
        "password": password,
        "rejectUnauthorized": not reject_unauthorized
    }

def manipulate_data(content):
    """
    Manipulation logic for fixed-width COBOL data.
    Goal: Remove Social Security Numbers (replace with spaces).
    Format:
    - Account: 8, Bill: 4, SSN: 11, Name: 30, Phone: 10, Email: 30 (Total: 93 chars)
    """
    manipulated_lines = []
    for line in content.splitlines():
        if len(line) < 93:
            manipulated_lines.append(line)
            continue
            
        account = line[0:8]
        bill = line[8:12]
        
        # Remove SSN (replace with 11 spaces)
        ssn = " " * 11
        
        # Keep Name, Phone, and Email as is from the original line
        name = line[23:53]
        phone = line[53:63]
        email = line[63:93]
        
        new_line = f"{account}{bill}{ssn}{name}{phone}{email}"
        manipulated_lines.append(new_line)
    
    return "\n".join(manipulated_lines)

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

@app.route('/manipulate-download', methods=['POST'])
def handle_manipulate_download():
    """
    Manipulates data and returns it in the response without uploading it back to the mainframe.
    """
    data = request.json
    input_ds = data.get('input_dataset')

    profile = get_profile_from_request(data)

    if not profile or not input_ds:
        return jsonify({"error": "Missing required fields"}), 400

    temp_in = "temp_in_dl.txt"

    try:
        datasets = Datasets(profile)
        datasets.perform_download(input_ds, temp_in)
        
        with open(temp_in, "r") as f:
            content = f.read()
            
        manipulated_content = manipulate_data(content)

        return jsonify({
            "status": "success",
            "manipulated_content": manipulated_content
        })
    except Exception as e:
        logging.error(f"Error during manipulation-download: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_in): os.remove(temp_in)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

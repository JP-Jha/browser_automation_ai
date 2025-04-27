
import base64
import os
import subprocess
import sys
import uuid

def create_directories():
    os.makedirs("recordings", exist_ok=True)
    os.makedirs("extracted_data", exist_ok=True)

def encode_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def run_subprocess(args):
    subprocess.run(args, check=True)

def automate_web_search(input_data):
    create_directories()
    url = input_data.get("url", "https://www.google.com")
    query = input_data.get("query", "")
    unique_id = str(uuid.uuid4())

    recording_file = f"recordings/recording_{unique_id}.webm"
    extracted_file = f"extracted_data/extracted_{unique_id}.txt"

    run_subprocess([
        sys.executable,
        "run_browser.py",
        "search",
        url,
        query,
        recording_file,
        extracted_file
    ])

    return {
        "video_file": {
            "name": os.path.basename(recording_file),
            "format": "webm",
            "data": encode_file(recording_file)
        },
        "extracted_file": {
            "name": os.path.basename(extracted_file),
            "format": "txt",
            "data": encode_file(extracted_file)
        }
    }

def search_flights(input_data):
    create_directories()
    source = input_data.get("source")
    destination = input_data.get("destination")
    departure_date = input_data.get("departure_date")
    return_date = input_data.get("return_date")
    adults = str(input_data.get("adults", 1))
    children = str(input_data.get("children", 0))
    unique_id = str(uuid.uuid4())

    recording_file = f"recordings/recording_{unique_id}.webm"
    extracted_file = f"extracted_data/extracted_{unique_id}.txt"

    run_subprocess([
        sys.executable,
        "run_browser.py",
        "flight",
        source,
        destination,
        departure_date,
        return_date,
        adults,
        children,
        recording_file,
        extracted_file
    ])

    return {
        "video_file": {
            "name": os.path.basename(recording_file),
            "format": "webm",
            "data": encode_file(recording_file)
        },
        "extracted_file": {
            "name": os.path.basename(extracted_file),
            "format": "txt",
            "data": encode_file(extracted_file)
        }
    }

def gmail_login(input_data):
    create_directories()
    email = input_data.get("email")
    password = input_data.get("password")
    unique_id = str(uuid.uuid4())

    recording_file = f"recordings/recording_{unique_id}.webm"
    extracted_file = f"extracted_data/extracted_{unique_id}.txt"

    run_subprocess([
        sys.executable,
        "run_browser.py",
        "gmail",
        email,
        password,
        recording_file,
        extracted_file
    ])

    return {
        "video_file": {
            "name": os.path.basename(recording_file),
            "format": "webm",
            "data": encode_file(recording_file)
        },
        "extracted_file": {
            "name": os.path.basename(extracted_file),
            "format": "txt",
            "data": encode_file(extracted_file)
        }
    }

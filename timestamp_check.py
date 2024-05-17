import os
import requests
import json
from datetime import datetime, timezone, timedelta
import re

def process_target_info(target):
    # Extract and print the commit_finder_hash and commit_finder_date
    commit_finder_hash = target.get('info', {}).get('commit_hash')
    commit_finder_date = target.get('info', {}).get('commit_date')

    print(f"Commit Finder Hash: {commit_finder_hash}")
    print(f"Commit Finder Date: {commit_finder_date}")
    
    return commit_finder_hash, commit_finder_date

def extract_group_and_artifact_id(info):
    full_name = info.get('full_name')
    if full_name:
        pattern = r'pkg:maven/([^/]+)/([^@]+)@'
        match = re.search(pattern, full_name)
        if match:
            group_id = match.group(1)
            artifact_id = match.group(2)
            return group_id, artifact_id
    return None, None

def get_latest_version_info(json_response):
    # Parse the JSON response
    data = json.loads(json_response)
    
    # Extract the list of documents (versions)
    docs = data['response']['docs']
    
    # Find the document with the latest timestamp
    latest_version_info = max(docs, key=lambda doc: doc['timestamp'])
    
    # Extract the version and timestamp
    latest_version = latest_version_info['v']
    latest_timestamp = latest_version_info['timestamp']
    
    # Convert the timestamp to ISO 8601 format
    dt = datetime.fromtimestamp(latest_timestamp / 1000, tz=timezone.utc)
    latest_timestamp_iso = dt.isoformat()
    
    return latest_version, latest_timestamp_iso

def fetch_maven_data(group_id, artifact_id):
    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=20&wt=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()

def compare_timestamps(commit_finder_date, maven_timestamp):
    # Convert commit_finder_date to datetime object
    commit_finder_datetime = datetime.fromisoformat(commit_finder_date)
    # Convert maven_timestamp to datetime object
    maven_datetime = datetime.fromisoformat(maven_timestamp)
    # Calculate the time difference
    time_difference = maven_datetime - commit_finder_datetime
    return time_difference

def is_time_difference_more_than_24_hours(time_difference):
    # Check if the time difference is more than 24 hours
    return time_difference > timedelta(hours=24)

def store_time_difference(package_name, time_difference, commit_finder_date, latest_timestamp, latest_version, json_file_name):
    with open('time.txt', 'a') as f:  # Open in append mode
        f.write(f"-----------------Time Information from {json_file_name}-----------------\n")
        f.write(f"Package Name - {package_name}\n")
        f.write(f"Commit Finder Date - {commit_finder_date}\n")
        f.write(f"Maven Timestamp - {latest_timestamp}\n")
        f.write(f"Time Difference - {time_difference}\n")
        f.write(f"Latest Version - {latest_version}\n")
        f.write(f"Time Difference > 24 hours: {is_time_difference_more_than_24_hours(time_difference)}\n")
        f.write("\n")  # Add a newline for better readability

def process_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {json_file_path}: {e}")
            return

    if isinstance(data, list):
        for target in data:
            process_target(target, os.path.basename(json_file_path))
    elif isinstance(data, dict):
        process_target(data, os.path.basename(json_file_path))
    else:
        print(f"Unexpected root type in {json_file_path}: {type(data)}")

def process_target(target, json_file_name):
    if not isinstance(target, dict):
        print(f"Unexpected target type: {type(target)}")
        return

    targets = target.get('target')
    if isinstance(targets, list):
        for item in targets:
            process_individual_target(item, json_file_name)
    elif isinstance(targets, dict):
        process_individual_target(targets, json_file_name)
    elif targets is None:
        print(f"Target is None in target: {target}")
    else:
        print(f"Unexpected 'target' type: {type(targets)}")

def process_individual_target(target, json_file_name):
    commit_finder_hash, commit_finder_date = process_target_info(target)
    group_id, artifact_id = extract_group_and_artifact_id(target.get('info', {}))
    if group_id and artifact_id and commit_finder_date:
        print(f"Group ID: {group_id}")
        print(f"Artifact ID: {artifact_id}")

        # Fetch and print the latest version info
        json_response = fetch_maven_data(group_id, artifact_id)
        latest_version, latest_timestamp = get_latest_version_info(json_response)

        print("Latest version:", latest_version)
        print("Timestamp:", latest_timestamp)
        
        # Compare the timestamps
        time_difference = compare_timestamps(commit_finder_date, latest_timestamp)
        package_name = f"{group_id}/{artifact_id}"
        
        # Store the information into time.txt
        store_time_difference(package_name, time_difference, commit_finder_date, latest_timestamp, latest_version, json_file_name)
    else:
        print(f"Could not extract group_id, artifact_id, or commit_finder_date from the JSON data: {target}")

def process_json_files_in_directory(directory):
    # Walk through all subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                process_json_file(json_file_path)

# Specify the directory containing JSON files
directory = r"C:\Users\anshu\Desktop\macaron\output\reports\maven"

# Process all JSON files in the directory and subdirectories
process_json_files_in_directory(directory)
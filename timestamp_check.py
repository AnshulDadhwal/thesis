import requests
import json
from datetime import datetime, timezone
import re

def print_commit_info(json_file):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract and print the commit_finder_hash and commit_finder_date
    commit_finder_hash = data.get('target', {}).get('info', {}).get('commit_hash')
    commit_finder_date = data.get('target', {}).get('info', {}).get('commit_date')

    print(f"Commit Finder Hash: {commit_finder_hash}")
    print(f"Commit Finder Date: {commit_finder_date}")

def extract_group_and_artifact_id(data):
    full_name = data.get('target', {}).get('info', {}).get('full_name')
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

def store_time_difference(package_name, time_difference, commit_finder_date, latest_version):
    with open('time.txt', 'a') as f:  # Open in append mode
        f.write("----------------------------------------Time Difference Information ------------------------------------------\n")
        f.write(f"Package Name - {package_name}\n")
        f.write(f"Time Difference - {time_difference}\n")
        f.write(f"Version from Commit Finder - {commit_finder_date}\n")
        f.write(f"Latest Version - {latest_version}\n")
        f.write("\n")  # Add a newline for better readability
    print("time.txt file was updated with the time difference information.")

# Test the function with a JSON file
json_file = 'caliper.json'
print_commit_info(json_file)

# Open the JSON file and load the data to extract group_id and artifact_id
with open(json_file, 'r') as f:
    data = json.load(f)
group_id, artifact_id = extract_group_and_artifact_id(data)

if group_id and artifact_id:
    print(f"Group ID: {group_id}")
    print(f"Artifact ID: {artifact_id}")

    # Fetch and print the latest version info
    json_response = fetch_maven_data(group_id, artifact_id)
    latest_version, latest_timestamp = get_latest_version_info(json_response)
    
    # Extract the commit_finder_date from the JSON file again
    commit_finder_date = data.get('target', {}).get('info', {}).get('commit_date')

    print("Latest version:", latest_version)
    print("Timestamp:", latest_timestamp)
    
    # Compare the timestamps
    if commit_finder_date:
        time_difference = compare_timestamps(commit_finder_date, latest_timestamp)
        package_name = f"{group_id}/{artifact_id}"
        
        # Store the information into time.txt
        store_time_difference(package_name, time_difference, commit_finder_date, latest_version)
else:
    print("Could not extract group_id and artifact_id from the JSON file.")

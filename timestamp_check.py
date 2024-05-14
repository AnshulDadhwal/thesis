import requests
import json
from datetime import datetime, timezone
import re

def print_commit_info(json_file):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract and print the commit_hash and commit_date
    commit_hash = data.get('target', {}).get('info', {}).get('commit_hash')
    commit_date = data.get('target', {}).get('info', {}).get('commit_date')

    print(f"Commit Hash: {commit_hash}")
    print(f"Commit Date: {commit_date}")

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

    print("Latest version:", latest_version)
    print("Timestamp:", latest_timestamp)
else:
    print("Could not extract group_id and artifact_id from the JSON file.")

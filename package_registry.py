import csv
import requests
import json

def fetch_versions(group_id, artifact_id):
    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=20&wt=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        versions = [doc['v'] for doc in data['response']['docs']]
        return versions
    except requests.RequestException as e:
        print(f"Error fetching data for {group_id}:{artifact_id} - {str(e)}")
        return []

def process_csv_file(filepath, output_file):
    with open(filepath, mode='r', newline='', encoding='utf-8') as file, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print(f"Skipping incomplete row: {row}")
                outfile.write(f"Incomplete format in row, skipped: {row}\n")
                continue
            try:
                group_id, artifact_id = row[1].split(':')
                versions = fetch_versions(group_id, artifact_id)
                if versions:
                    outfile.write(f"{group_id}:{artifact_id} - Versions: {', '.join(versions)}\n")
                else:
                    outfile.write(f"{group_id}:{artifact_id} - No versions found\n")
            except ValueError:
                print(f"Skipping invalid row: {row}")
                outfile.write(f"Invalid format in row, skipped: {row}\n")

# Replace 'path_to_your_csv_file.csv' and 'output_file.txt' with actual paths
process_csv_file('./maven_150.csv', './maven_versions.txt')

def print_commit_info(json_file):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract and print the commit_hash and commit_date
    commit_hash = data.get('target', {}).get('info', {}).get('commit_hash')
    commit_date = data.get('target', {}).get('info', {}).get('commit_date')

    print(f"Commit Hash: {commit_hash}")
    print(f"Commit Date: {commit_date}")

# Test the function with a JSON file
print_commit_info('caliper.json')

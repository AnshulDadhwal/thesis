import csv
import requests

def fetch_latest_version(group_id, artifact_id):
    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=1&wt=json&sort=version+desc"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['response']['docs']:
            latest_version = data['response']['docs'][0]['v']
            return latest_version
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching data for {group_id}:{artifact_id} - {str(e)}")
        return None

def process_csv_file(filepath, output_file):
    with open(filepath, mode='r', newline='', encoding='utf-8') as file, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(file)
        writer = csv.writer(outfile)
        writer.writerow(['group_id', 'artifact_id', 'version'])  # Write header
        for row in reader:
            if len(row) < 2:
                print(f"Skipping incomplete row: {row}")
                continue
            try:
                group_id, artifact_id = row[1].split(':')
                latest_version = fetch_latest_version(group_id, artifact_id)
                if latest_version:
                    writer.writerow([group_id, artifact_id, latest_version])
                else:
                    writer.writerow([group_id, artifact_id, 'No version found'])
            except ValueError:
                print(f"Skipping invalid row: {row}")

# Replace 'path_to_your_csv_file.csv' and 'output_file.csv' with actual paths
process_csv_file('./maven_150.csv', './maven_latest_versions.csv')

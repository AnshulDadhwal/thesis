import csv
import subprocess
import os

# File path
csv_file_path = './maven_latest_versions.csv'

def run_commands_from_csv():
    # Ensure the CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    # Read the CSV file
    try:
        with open(csv_file_path, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip header row
            packages = list(reader)
            print(f"CSV read successfully: {len(packages)} packages found.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    for package in packages:
        group_id = package[0]
        artifact_id = package[1]
        version = package[2]
        full_purl = f"pkg:maven/{group_id}/{artifact_id}@{version}"

        # Run the command
        command = f"./run_macaron.sh analyze -purl {full_purl} --skip-deps"
        print(f"Running command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, executable='/bin/bash')
            # Print the command output for logging purposes
            print(result.stdout.decode('utf-8'))
            print(result.stderr.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error output: {e.stderr.decode('utf-8')}")
        except Exception as e:
            print(f"Error running subprocess: {e}")

if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")
    run_commands_from_csv()

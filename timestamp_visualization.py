import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def parse_time_info(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        
    time_info_pattern = re.compile(
        r'Package Name - (?P<package_name>.*?)\n'
        r'Commit Finder Date - (?P<commit_date>.*?)\n'
        r'Maven Timestamp - (?P<maven_date>.*?)\n'
        r'Time Difference - (?P<time_difference>.*?)\n'
        r'Latest Version - (?P<latest_version>.*?)\n'
        r'Time Difference > 24 hours: (?P<greater_than_24>.*?)\n'
    )
    
    matches = time_info_pattern.findall(data)
    time_info_list = []

    for match in matches:
        package_name, commit_date, maven_date, time_difference, latest_version, greater_than_24 = match
        commit_date = datetime.fromisoformat(commit_date)
        maven_date = datetime.fromisoformat(maven_date)
        
        # Parse time difference
        time_difference_parts = time_difference.split(', ')
        days, time_part = 0, time_difference_parts[0]
        if len(time_difference_parts) == 2:
            days, time_part = int(time_difference_parts[0].split(' ')[0]), time_difference_parts[1]
        hours, minutes, seconds = map(float, time_part.split(':'))
        time_difference_td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        
        greater_than_24 = greater_than_24 == 'True'
        
        time_info_list.append({
            'package_name': package_name,
            'commit_date': commit_date,
            'maven_date': maven_date,
            'time_difference': time_difference_td,
            'latest_version': latest_version,
            'greater_than_24': greater_than_24
        })
    
    return time_info_list

def plot_time_differences_bar(time_info_list):
    package_names = [info['package_name'] for info in time_info_list]
    time_differences = [info['time_difference'].total_seconds() / 3600 for info in time_info_list]
    greater_than_24 = [info['greater_than_24'] for info in time_info_list]
    
    plt.figure(figsize=(12, 8))
    colors = ['red' if gt24 else 'green' for gt24 in greater_than_24]
    
    plt.bar(package_names, time_differences, color=colors)
    plt.axhline(y=24, color='blue', linestyle='--', label='24 hours')
    plt.yscale('log')
    plt.xlabel('Package Name')
    plt.ylabel('Time Difference (hours) [Log scale]')
    plt.title('Time Differences between Commit Finder Date and Maven Timestamp')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()
    

def main():
    file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\thesis\time.txt"
    time_info_list = parse_time_info(file_path)
    plot_time_differences_bar(time_info_list)

if __name__ == "__main__":
    main()

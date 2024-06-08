import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# Load the workbook and read sheet names
file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\pypi100.xlsx"

try:
    workbook = load_workbook(filename=file_path)
    sheet_names = workbook.sheetnames
    print("Sheet names:", sheet_names)
    
    # Load the first sheet
    sheet = workbook[sheet_names[0]]
    
    # Initialize a list to store rows
    data = []

    # Iterate over rows in the sheet and collect data
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    
    # Convert to DataFrame
    columns = data[0]  # First row as columns
    df = pd.DataFrame(data[1:], columns=columns)
    df.columns = [str(col).strip() for col in df.columns]  # Clean column names
    print("Columns in DataFrame:", df.columns)
    print(df.head())
    
    # Bar Chart: Correct vs Incorrect Repository Links
    repo_correctness = df['Is the repo link correct?'].value_counts()
    plt.figure(figsize=(10, 6))
    repo_correctness.plot(kind='bar', color=['#67ede7', '#fce85d', '#ff9933'])  # Lighter green and orange
    plt.title('Correct vs Incorrect Repository Links (PyPI)')
    plt.xlabel('Repository Link Correctness')
    plt.ylabel('Number of Packages')
    plt.xticks(rotation=0)
    plt.grid(axis='y', alpha=0.3)  # Add gridlines to the y-axis with less opacity
    plt.show()

    # Pie Chart: Packages Having the Repository as a Related Package
    related_package_repo = df['Does it have the repo as related package?'].value_counts()
    plt.figure(figsize=(8, 8))
    related_package_repo.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#aaf42c', '#52f24a'])  # Light blue and light green
    plt.title('Packages declaring the main repository in their metadata (PyPI)')
    plt.ylabel('')
    plt.show()

    # Pie Chart: Correctness of PyPI package registry link collected by deps.dev
    registry_link_correctness = df['Is it correct?'].value_counts()
    plt.figure(figsize=(8, 8))
    registry_link_correctness.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff3377', '#4c00a4'])  # Light pink and light cyan
    plt.title('Correctness of PyPI package registry link collected by deps.dev')
    plt.ylabel('')
    plt.show()

except Exception as e:
    print(f"Error: {e}")

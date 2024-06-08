import pandas as pd
import matplotlib.pyplot as plt

# Specify the path to your Excel file
file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\Maven100.xlsx"

# Load the data from the Excel file
xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

# Load a specific sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')  # replace 'Sheet1' with the actual sheet name

# Display the shape of the DataFrame to confirm all rows are loaded
print(f"DataFrame shape: {df.shape}")

# Display the first few rows of the DataFrame
print(df.head())

# Convert missing values to 'N/A'
df['Is the repo link correct?'] = df['Is the repo link correct?'].fillna('N/A')
df['Does it have the repo as related package?'] = df['Does it have the repo as related package?'].fillna('N/A')
df['Is the origin link correct (Maven Central)?'] = df['Is the origin link correct (Maven Central)?'].fillna('N/A')

# Bar Chart: Correct vs Incorrect Repository Links
repo_correctness = df['Is the repo link correct?'].value_counts().reindex(['Yes', 'No', 'N/A'], fill_value=0)
print("Repository Link Correctness Counts:")
print(repo_correctness)

plt.figure(figsize=(10, 6))
repo_correctness.plot(kind='bar', color=['#67ede7', '#fce85d', '#ff9933'])  # Lighter colors
plt.title('Correct vs Incorrect Repository Links (Maven)')
plt.xlabel('Repository Link Correctness')
plt.ylabel('Number of Packages')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)  # Add gridlines to the y-axis with less opacity
plt.show()

# Pie Chart: Packages Having the Repository as a Related Package
related_package_repo = df['Does it have the repo as related package?'].value_counts().reindex(['Yes', 'No', 'N/A'], fill_value=0)
print("Related Package Repository Counts:")
print(related_package_repo)

plt.figure(figsize=(8, 8))
related_package_repo.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#aaf42c', '#52f24a', '#28df7e']) 
plt.title('Packages declaring the main repository in their metadata (Maven)')
plt.ylabel('')
plt.show()

# Pie Chart: Correctness of Maven Central origin link
origin_link_correctness = df['Is the origin link correct (Maven Central)?'].value_counts()
print("Maven Central Origin Link Correctness Counts:")
print(origin_link_correctness)

plt.figure(figsize=(8, 8))
origin_link_correctness.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff3377', '#4c00a4'])  # Light pink and light cyan
plt.title('Correctness of Maven Central origin link')
plt.ylabel('')
plt.show()

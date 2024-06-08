import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\npm100.xlsx"

# Load the data from the Excel file
xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

# Load a specific sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')  # replace 'Sheet1' with the actual sheet name if different

# Display the shape of the DataFrame to confirm all rows are loaded
print(f"DataFrame shape: {df.shape}")

# Display the first few rows of the DataFrame
print(df.head())

# Bar Chart: Correct vs Incorrect Repository Links
repo_correctness = df['Is the repo link correct?'].value_counts()

plt.figure(figsize=(10, 6))
repo_correctness.plot(kind='bar', color=['#67ede7', '#fce85d', '#ff9933'])  # Lighter green, yellow, and orange
plt.title('Correct vs Incorrect Repository Links (npm)')
plt.xlabel('Repository Link Correctness')
plt.ylabel('Number of Packages')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)  # Add gridlines to the y-axis with less opacity
plt.show()

# Pie Chart: Packages Having the Repository as a Related Package
related_package_repo = df['Does it have the repo as related package?'].value_counts()

plt.figure(figsize=(8, 8))
related_package_repo.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#aaf42c', '#52f24a'])  # Light green shades
plt.title('Packages Declaring the Main Repository in Their Metadata (npm)')
plt.ylabel('')
plt.show()

# Pie Chart: Correctness of Origin Links (npmjs)
origin_link_correctness = df['Is the origin link correct (npmjs)?'].value_counts()

plt.figure(figsize=(8, 8))
origin_link_correctness.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff3377', '#4c00a4'])  # Pink and purple
plt.title('Correctness of Origin Links (npm)')
plt.ylabel('')
plt.show()

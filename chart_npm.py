import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\npm100.xlsx"

xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

df = pd.read_excel(file_path, sheet_name='Sheet1')

print(f"DataFrame shape: {df.shape}")

print(df.head())

repo_correctness = df['Is the repo link correct?'].value_counts()

plt.figure(figsize=(10, 6))
repo_correctness.plot(kind='bar', color=['#67ede7', '#fce85d', '#ff9933'])
plt.title('Correct vs Incorrect Repository Links (npm)')
plt.xlabel('Repository Link Correctness')
plt.ylabel('Number of Packages')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.show()

related_package_repo = df['Does it have the repo as related package?'].value_counts()

plt.figure(figsize=(8, 8))
related_package_repo.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#aaf42c', '#52f24a'])  
plt.title('Packages Declaring the Main Repository in Their Metadata (npm)')
plt.ylabel('')
plt.show()

origin_link_correctness = df['Is the origin link correct (npmjs)?'].value_counts()

plt.figure(figsize=(8, 8))
origin_link_correctness.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff3377', '#4c00a4'])  
plt.title('Correctness of Origin Links (npm)')
plt.ylabel('')
plt.show()

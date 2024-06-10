import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\Maven100.xlsx"

xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

df = pd.read_excel(file_path, sheet_name='Sheet1')

print(f"DataFrame shape: {df.shape}")

print(df.head())

df['Is the repo link correct?'] = df['Is the repo link correct?'].fillna('N/A')
df['Does it have the repo as related package?'] = df['Does it have the repo as related package?'].fillna('N/A')
df['Is the origin link correct (Maven Central)?'] = df['Is the origin link correct (Maven Central)?'].fillna('N/A')

repo_correctness = df['Is the repo link correct?'].value_counts().reindex(['Yes', 'No', 'N/A'], fill_value=0)

plt.figure(figsize=(10, 6))
repo_correctness.plot(kind='bar', color=['#67ede7', '#fce85d', '#ff9933'])
plt.title('Correct vs Incorrect Repository Links (Maven)')
plt.xlabel('Repository Link Correctness')
plt.ylabel('Number of Packages')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.show()

related_package_repo = df['Does it have the repo as related package?'].value_counts().reindex(['Yes', 'No'], fill_value=0)

plt.figure(figsize=(8, 8))
related_package_repo.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#aaf42c', '#52f24a', '#28df7e']) 
plt.title('Packages declaring the main repository in their metadata (Maven)')
plt.ylabel('')
plt.show()

origin_link_correctness = df['Is the origin link correct (Maven Central)?'].value_counts()

plt.figure(figsize=(8, 8))
origin_link_correctness.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff3377', '#4c00a4'])
plt.title('Correctness of Maven Central origin link')
plt.ylabel('')
plt.show()

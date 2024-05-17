import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel files
maven_df = pd.read_excel(r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\Maven100.xlsx")
npm_df = pd.read_excel(r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\npm100.xlsx")
pypi_df = pd.read_excel(r"C:\Users\anshu\Desktop\Anshul\University\University of Queensland\REIT4842 - R&D Methods and Practice\Proposal Draft\pypi100.xlsx")

# Convert 'Yes'/'No' to boolean values
maven_df['Is the repo link correct?'] = maven_df['Is the repo link correct?'].map({'Yes': True, 'No': False})
npm_df['Is the repo link correct?'] = npm_df['Is the repo link correct?'].map({'Yes': True, 'No': False})
pypi_df['Is the repo link correct?'] = pypi_df['Is the repo link correct?'].map({'Yes': True, 'No': False})

# Calculate the counts of correct and incorrect repositories for each package registry
maven_correct = maven_df['Is the repo link correct?'].sum()
maven_incorrect = len(maven_df) - maven_correct

npm_correct = npm_df['Is the repo link correct?'].sum()
npm_incorrect = len(npm_df) - npm_correct

pypi_correct = pypi_df['Is the repo link correct?'].sum()
pypi_incorrect = len(pypi_df) - pypi_correct

# Prepare data for the bar chart
data = {
    'Maven': [maven_correct, maven_incorrect],
    'NPM': [npm_correct, npm_incorrect],
    'PyPI': [pypi_correct, pypi_incorrect]
}

# Create a dataframe for plotting
plot_df = pd.DataFrame(data, index=['Correct', 'Incorrect'])

# Plot the bar chart
plot_df.plot(kind='bar', figsize=(10, 6), color=['orange', 'blue', 'green'])
plt.title('Correct vs Incorrect Repositories by Package Registry')
plt.xlabel('Repository Status')
plt.ylabel('Number of Repositories')
plt.xticks(rotation=0)
plt.legend(title='Package Registry')
plt.show()

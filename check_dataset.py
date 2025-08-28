import pandas as pd

# Load the merged dataset
df = pd.read_csv("urls_dataset.csv")

# Preview first 5 rows
print("Preview of dataset:")
print(df.head())

# Count phishing vs legitimate
print("\nLabel counts:")
print(df['label'].value_counts())
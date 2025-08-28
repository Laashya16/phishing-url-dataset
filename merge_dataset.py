import pandas as pd

# Load phishing and legitimate datasets
phish_df = pd.read_csv("phishing.csv")
legit_df = pd.read_csv("legitimate.csv")

# Add labels: 1 for phishing, 0 for legitimate
phish_df["label"] = 1
legit_df["label"] = 0

# Combine both datasets
merged_df = pd.concat([phish_df, legit_df], ignore_index=True)

# Shuffle rows to mix phishing & legit examples
merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save as a new file
merged_df.to_csv("merged_dataset.csv", index=False)
print("✅ Merged dataset saved as merged_dataset.csv")

# Preview first few rows
print(merged_df.head())
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("cleaned_urls.csv")

# Make sure the label column is named 'label' (1 = phishing, 0 = legitimate)
print("Unique labels in dataset:", df['label'].unique())

# Split into phishing and legitimate
phishing_df = df[df['label'] == 1]
legitimate_df = df[df['label'] == 0]

# Save them separately
phishing_df.to_csv("phishing_urls.csv", index=False)
legitimate_df.to_csv("legitimate_urls.csv", index=False)

print("✅ Files saved: phishing_urls.csv and legitimate_urls.csv")
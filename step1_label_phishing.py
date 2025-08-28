import pandas as pd

# Load your cleaned phishing URLs file
df = pd.read_csv("cleaned_urls.csv")

# Add a new column called 'label' with 1 for phishing
df["label"] = 1

# Save it to a new file
df.to_csv("phishing_urls_labeled.csv", index=False)

print("✅ phishing_urls_labeled.csv created with", len(df), "rows")
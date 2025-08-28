import pandas as pd
import numpy as np
import sys

def extract_features(url):
    """
    Simple example feature extractor.
    Replace this with your real feature extraction logic
    (like SSL info, redirects, length, etc.).
    """
    features = {}
    features['url_length'] = len(url)
    features['has_https'] = 1 if url.startswith("https") else 0
    return features

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python feature_extraction.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Load dataset
    df = pd.read_csv(input_file)

    # Drop missing/NaN URLs
    df = df.dropna(subset=['url'])
    df['url'] = df['url'].astype(str)

    # Extract features for each URL
    feature_rows = []
    for _, row in df.iterrows():
        url = row['url']
        label = row['label']
        feats = extract_features(url)
        feats['url'] = url
        feats['label'] = label
        feature_rows.append(feats)

    # Convert to DataFrame
    features_df = pd.DataFrame(feature_rows)

    # Save final feature dataset
    features_df.to_csv(output_file, index=False)
    print(f"✅ Features saved to {output_file}")
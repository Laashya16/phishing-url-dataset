# clean_dataset.py
import os
import sys
import traceback
import pandas as pd
import re

INPUT = "urls_dataset.csv"
OUTPUT = "cleaned_urls.csv"

def try_read(path):
    # Try several safe read options
    exceptions = []
    for enc in (None, "utf-8-sig", "latin1"):
        try:
            # engine="python" + comment="#" helps skip URLhaus-style header lines
            return pd.read_csv(path, encoding=enc, comment="#", engine="python")
        except Exception as e:
            exceptions.append((enc, repr(e)))
    # last fallback: try reading with no header to inspect raw rows
    raise Exception("All read attempts failed. Tried encodings: " + str(exceptions))


def detect_url_column(df):
    # normalize column names for matching
    cols = [str(c).strip().lower() for c in df.columns.tolist()]

    # common candidates
    candidates = ["url", "uri", "link", "website", "domain", "host", "address"]
    for cand in candidates:
        for i, c in enumerate(cols):
            if cand == c or cand in c:
                return df.columns[i]

    # fallback: peek at first column values — detect if they look like URLs
    first_col = df.columns[0]
    sample = df[first_col].astype(str).dropna().head(20).tolist()
    url_like = re.compile(r"^\s*https?://", re.I)
    score = sum(1 for s in sample if url_like.search(s))
    if score >= 1:
        return first_col

    return None


def clean_and_save(df, url_col):
    # keep just the url column, normalize, drop empties/dupes
    out = df[[url_col]].copy()
    out.columns = ["url"]
    out["url"] = out["url"].astype(str).str.strip()
    out = out[out["url"] != ""]
    out = out.drop_duplicates(subset=["url"]).reset_index(drop=True)
    out.to_csv(OUTPUT, index=False)
    return out


def main():
    if not os.path.exists(INPUT):
        print(f"❌ Input file '{INPUT}' not found in: {os.getcwd()}")
        print("Make sure urls_dataset.csv is in this folder, or update INPUT variable in the script.")
        sys.exit(1)

    try:
        df = try_read(INPUT)
    except Exception as e:
        print("❌ Failed to read the CSV file. Error details:")
        print(e)
        traceback.print_exc()
        sys.exit(1)

    print("Detected columns:", list(df.columns))

    url_col = detect_url_column(df)
    if url_col is None:
        print("\n❌ Could not auto-detect a URL column.")
        print("Here are the first 10 rows (for you to inspect):\n")
        print(df.head(10).to_string(index=False))
        print("\nPlease tell me which column contains the URLs (copy exact column name) or rename it to 'url'.")
        sys.exit(1)

    print(f"\n✅ Using column: '{url_col}' as the URL column.")
    cleaned = clean_and_save(df, url_col)
    print(f"\n✅ Saved {len(cleaned)} unique, non-empty URLs to '{OUTPUT}'.")
    print("\nPreview (first 10 rows):")
    print(cleaned.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
import sys
import pandas as pd
from dynamic_analyzer import analyze_url  # adjust import if needed

def run_batch(input_file, output_file):
    # Load CSV
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Error reading {input_file}: {e}")
        return

    # Try to detect URL column automatically
    url_column = None
    for col in df.columns:
        if "url" in col.lower():  # match url, URL, urlhaus, etc.
            url_column = col
            break

    if url_column is None:
        print("❌ No URL-like column found. Available columns:", df.columns.tolist())
        return

    print(f"✅ Using column '{url_column}' for URLs")

    # Extract URLs
    urls = df[url_column].dropna().tolist()
    print(f"🔎 Found {len(urls)} URLs to analyze")

    results = []
    for url in urls:
        try:
            result = analyze_url(url)
            results.append(result)
        except Exception as e:
            print(f"⚠ Error analyzing {url}: {e}")

    # Save results
    if results:
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)
        print(f"✅ Analysis complete. Results saved to {output_file}")
    else:
        print("⚠ No results to save.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_batch.py <input_csv> <output_csv>")
    else:
        run_batch(sys.argv[1], sys.argv[2])
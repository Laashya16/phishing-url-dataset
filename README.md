
# Phishing URL Dataset & Preprocessing Pipeline

## 📌 Overview
This repository contains datasets and preprocessing scripts for phishing URL detection.  
The goal is to provide a clean, structured dataset with extracted features that can be directly used by ML Engineers to train models.

---

## 📂 Repository Structure

├── phishing.csv            # Raw phishing URLs dataset ├── legitimate.csv          # Raw legitimate URLs dataset ├── merged_dataset.csv      # Combined dataset of phishing + legitimate ├── final_features.csv      # Final cleaned dataset with extracted features ├── clean.py                # Script to clean and prepare raw URLs ├── merge_dataset.py        # Script to merge phishing + legitimate datasets ├── feature_extraction.py   # Script to extract features from merged dataset └── README.md               # Project documentation

---

## ⚙️ Steps Completed (Data Engineering Workflow)
1. **Dataset Acquisition**  
   - Collected phishing and legitimate URLs.  

2. **Data Cleaning**  
   - Removed duplicates and standardized URL formats (`clean.py`).  

3. **Dataset Merging**  
   - Combined phishing + legitimate datasets into `merged_dataset.csv` (`merge_dataset.py`).  

4. **Feature Extraction**  
   - Generated additional features (length, number of dots, special chars, etc.)  
   - Saved into `final_features.csv` (`feature_extraction.py`).  

---

## 📊 Current Output
- **final_features.csv** is ready with columns:  
  - `url`  
  - `label` (1 = phishing, 0 = legitimate)  
  - Extracted features (length, digits, symbols, etc.)  

---

## 🚀 Next Steps (For ML Engineer)
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/phishing-url-dataset.git
   cd phishing-url-dataset

2. Load final_features.csv into Python for training:

import pandas as pd

df = pd.read_csv("final_features.csv")
print(df.head())


3. Train models (Logistic Regression, Random Forest, XGBoost, etc.).


4. Evaluate and optimize for accuracy, precision, recall, F1-score.




---

🙌 Credits

Data Engineering by [Laashya16].
ML Engineering pending.

---

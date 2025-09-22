import pandas as pd
import re
import json
from datetime import datetime

# === 1. Load dataset ===
# Hard-coded path (change if needed)
file_path = r"C:\Users\Admin\OneDrive\Desktop\DA INTERN\Mall_Customers.csv.zip"

# Read as DataFrame
df = pd.read_csv(file_path)
raw_df = df.copy()

print("\n--- Initial inspection ---")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nMissing values:\n", df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

# === 2. Clean column names ===
df.columns = [re.sub(r'[^a-z0-9]+', '_', c.strip().lower()) for c in df.columns]

# Rename to nice names if they exist
df = df.rename(columns={
    "customerid": "customer_id",
    "gender": "gender",
    "age": "age",
    "annual_income_k": "annual_income",
    "spending_score_1_100": "spending_score"
})

# === 3. Handle missing values ===
df = df.dropna(subset=["customer_id"])  # drop rows without ID
df = df.fillna({
    "gender": "Unknown",
    "age": df["age"].median() if "age" in df else None,
    "annual_income": df["annual_income"].median() if "annual_income" in df else None,
    "spending_score": df["spending_score"].median() if "spending_score" in df else None,
})

# === 4. Remove duplicates ===
df = df.drop_duplicates()

# === 5. Standardize text values ===
if "gender" in df.columns:
    df["gender"] = df["gender"].str.strip().str.lower().replace({
        "male": "Male", "m": "Male",
        "female": "Female", "f": "Female"
    })

# === 6. Fix data types ===
if "age" in df.columns:
    df["age"] = df["age"].astype(int)

if "annual_income" in df.columns:
    df["annual_income"] = pd.to_numeric(df["annual_income"], errors="coerce").astype(int)

if "spending_score" in df.columns:
    df["spending_score"] = pd.to_numeric(df["spending_score"], errors="coerce").astype(int)

# === 7. Save cleaned dataset ===
out_path = r"C:\Users\Admin\OneDrive\Desktop\DA INTERN\mallcustomers_cleaned.csv"
df.to_csv(out_path, index=False)

# === 8. Print summary ===
print("\n--- Summary of Cleaning ---")
print("Original shape:", raw_df.shape)
print("Cleaned shape:", df.shape)
print("Columns after cleaning:", df.columns.tolist())
print("Cleaned file saved as:", out_path)

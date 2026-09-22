"""
Load the raw Telco customer export, clean it, and load it into a SQLite
database so the SQL scripts in /sql can run against it directly.
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "telco_churn.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "customers_clean.csv"
DB_PATH = ROOT / "db" / "retention.db"


def main():
    df = pd.read_csv(RAW_PATH)

    # TotalCharges is stored as text and is blank for a small number of
    # customers with tenure == 0 (brand new accounts that haven't been
    # billed yet). They can't churn or carry risk yet, so we exclude them
    # rather than impute a number that doesn't mean anything for them.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["TotalCharges"]).copy()
    dropped = before - len(df)

    df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})
    df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

    # "No internet service" / "No phone service" are logically just "No"
    # for these columns, and are perfectly collinear with InternetService /
    # PhoneService if left as a separate category -- that breaks logistic
    # regression (singular matrix). Collapsing them keeps the meaning and
    # removes the redundant category.
    collapse_cols = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies",
    ]
    for col in collapse_cols:
        df[col] = df[col].replace("No internet service", "No")
    df["MultipleLines"] = df["MultipleLines"].replace("No phone service", "No")

    bins = [-1, 12, 24, 48, 72]
    labels = ["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"]
    df["TenureBucket"] = pd.cut(df["tenure"], bins=bins, labels=labels)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("customers", conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} customers (dropped {dropped} zero-tenure rows with no billing history).")
    print(f"Clean CSV  -> {PROCESSED_PATH}")
    print(f"SQLite DB  -> {DB_PATH}")


if __name__ == "__main__":
    main()

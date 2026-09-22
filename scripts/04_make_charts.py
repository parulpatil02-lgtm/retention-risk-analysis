"""
Two charts for the one-page memo: churn rate by contract type, and churn
rate by tenure bucket. Kept deliberately simple -- these need to make
sense to a non-technical reader in under five seconds.
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "retention.db"
ASSETS = ROOT / "memo" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

ACCENT = "#1F6F5C"
INK = "#1B211D"


def main():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM customers", conn)

    by_contract = df.groupby("Contract")["ChurnFlag"].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(by_contract.index, by_contract.values, color=ACCENT)
    ax.set_ylabel("Churn rate (%)")
    ax.set_title("Churn rate by contract type", color=INK, fontweight="bold")
    ax.bar_label(bars, fmt="%.1f%%")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(ASSETS / "churn_by_contract.png", dpi=160)
    plt.close(fig)

    order = ["0-12 mo", "13-24 mo", "25-48 mo", "49-72 mo"]
    by_tenure = df.groupby("TenureBucket", observed=True)["ChurnFlag"].mean().reindex(order) * 100
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(by_tenure.index, by_tenure.values, color=ACCENT)
    ax.set_ylabel("Churn rate (%)")
    ax.set_title("Churn rate by tenure", color=INK, fontweight="bold")
    ax.bar_label(bars, fmt="%.1f%%")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(ASSETS / "churn_by_tenure.png", dpi=160)
    plt.close(fig)

    print(f"Saved charts to {ASSETS}")


if __name__ == "__main__":
    main()

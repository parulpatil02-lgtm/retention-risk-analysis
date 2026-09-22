"""
Which factors actually correlate with churn, and are they statistically
significant? Fits a logistic regression and runs chi-square tests on the
key categorical variables, so every claim in the memo is defensible.
"""
import sqlite3
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "retention.db"
OUT_COEF = ROOT / "data" / "processed" / "churn_driver_coefficients.csv"
OUT_CHI2 = ROOT / "data" / "processed" / "chi_square_tests.csv"

FEATURES = [
    "tenure",
    "MonthlyCharges",
    "Contract",
    "InternetService",
    "TechSupport",
    "OnlineSecurity",
    "PaperlessBilling",
    "PaymentMethod",
    "SeniorCitizen",
    "Dependents",
]
CATEGORICAL_FOR_CHI2 = [
    "Contract",
    "InternetService",
    "TechSupport",
    "OnlineSecurity",
    "PaperlessBilling",
    "PaymentMethod",
    "SeniorCitizen",
    "Dependents",
]


def main():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM customers", conn)

    # --- Chi-square tests: is each categorical variable independent of churn? ---
    chi2_rows = []
    for col in CATEGORICAL_FOR_CHI2:
        table = pd.crosstab(df[col], df["Churn"])
        chi2, p, _, _ = chi2_contingency(table)
        chi2_rows.append({"variable": col, "chi2": round(chi2, 2), "p_value": round(p, 6)})
    chi2_df = pd.DataFrame(chi2_rows).sort_values("p_value")
    OUT_CHI2.parent.mkdir(parents=True, exist_ok=True)
    chi2_df.to_csv(OUT_CHI2, index=False)

    # --- Logistic regression: direction and size of each effect ---
    X = pd.get_dummies(df[FEATURES], drop_first=True)
    X = sm.add_constant(X).astype(float)
    y = df["ChurnFlag"].astype(float)

    model = sm.Logit(y, X).fit(disp=False)
    coef_df = pd.DataFrame(
        {
            "variable": model.params.index,
            "coefficient": model.params.values,
            "odds_ratio": pd.Series(model.params).apply(lambda b: round(2.71828 ** b, 3)),
            "p_value": model.pvalues.values,
        }
    )
    coef_df = coef_df[coef_df["variable"] != "const"].sort_values("p_value")
    coef_df.to_csv(OUT_COEF, index=False)

    print("=== Chi-square tests (lower p_value = stronger association with churn) ===")
    print(chi2_df.to_string(index=False))
    print("\n=== Logistic regression: top significant drivers (p < 0.05) ===")
    print(coef_df[coef_df["p_value"] < 0.05].to_string(index=False))
    print(f"\nModel pseudo R-squared: {model.prsquared:.3f}")
    print(f"\nSaved -> {OUT_COEF}")
    print(f"Saved -> {OUT_CHI2}")


if __name__ == "__main__":
    main()

"""
Train a churn model on historical customers (who we already know churned
or stayed), validate it on a held-out set, then SCORE ONLY CURRENTLY
ACTIVE CUSTOMERS with it -- that's the realistic version of this task:
a retention team doesn't need a prediction for someone who already left.
"""
import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "retention.db"
OUT_RANKED = ROOT / "data" / "processed" / "revenue_at_risk_ranked.csv"
OUT_SUMMARY = ROOT / "data" / "processed" / "revenue_at_risk_summary.csv"
OUT_SCENARIOS = ROOT / "data" / "processed" / "impact_scenarios.csv"

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
TOP_N = 150


def build_design_matrix(df, reference_columns=None):
    X = pd.get_dummies(df[FEATURES], drop_first=True).astype(float)
    if reference_columns is not None:
        X = X.reindex(columns=reference_columns, fill_value=0.0)
    return X


def main():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT * FROM customers", conn)

    X_all = build_design_matrix(df)
    y_all = df["ChurnFlag"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y_all, test_size=0.2, random_state=42, stratify=y_all
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    test_scores = pd.Series(model.predict_proba(X_test)[:, 1], index=X_test.index)
    test_auc = roc_auc_score(y_test, test_scores)

    # Does the ranking concentrate real churn? Measured on customers the model
    # never saw: actual churn among its top-scored 10% vs the overall rate.
    top_test_idx = test_scores.nlargest(round(len(y_test) * 0.10)).index
    base_rate = y_test.mean()
    top_decile_rate = y_test.loc[top_test_idx].mean()
    churners_captured = y_test.loc[top_test_idx].sum() / y_test.sum()

    # Refit on all historical data for the deployed scoring model.
    model.fit(X_all, y_all)

    active = df[df["Churn"] == "No"].copy()
    X_active = build_design_matrix(active, reference_columns=X_all.columns)
    active["churn_probability"] = model.predict_proba(X_active)[:, 1]
    active["annual_revenue"] = active["MonthlyCharges"] * 12
    active["revenue_at_risk"] = active["churn_probability"] * active["annual_revenue"]

    ranked = active.sort_values("revenue_at_risk", ascending=False).reset_index(drop=True)
    ranked["risk_rank"] = ranked.index + 1

    cols = [
        "risk_rank",
        "customerID",
        "Contract",
        "InternetService",
        "tenure",
        "MonthlyCharges",
        "annual_revenue",
        "churn_probability",
        "revenue_at_risk",
    ]
    top = ranked[cols].head(TOP_N)
    OUT_RANKED.parent.mkdir(parents=True, exist_ok=True)
    top.to_csv(OUT_RANKED, index=False)

    # Illustrative scenarios, NOT predictions: no retention campaign was run.
    # If an offer saves a share of the accounts expected to churn, this is the
    # revenue kept, and the most the offer can cost per contacted account
    # before it stops paying for itself.
    expected_at_risk = top["revenue_at_risk"].sum()
    scenarios = pd.DataFrame(
        [
            {
                "assumed_save_rate": rate,
                "annual_revenue_retained": round(expected_at_risk * rate, 2),
                "breakeven_offer_cost_per_account": round(expected_at_risk * rate / TOP_N, 2),
            }
            for rate in (0.10, 0.20, 0.30)
        ]
    )
    scenarios.to_csv(OUT_SCENARIOS, index=False)

    random_list_at_risk = active["revenue_at_risk"].mean() * TOP_N

    summary = pd.DataFrame(
        [
            {
                "held_out_test_auc": round(test_auc, 3),
                "held_out_base_churn_rate": round(base_rate, 3),
                "held_out_top_decile_churn_rate": round(top_decile_rate, 3),
                "held_out_top_decile_lift": round(top_decile_rate / base_rate, 2),
                "held_out_churners_in_top_decile": round(churners_captured, 3),
                "expected_at_risk_random_list_same_size": round(random_list_at_risk, 2),
                "targeting_advantage_vs_random": round(expected_at_risk / random_list_at_risk, 2),
                "active_customers_scored": len(active),
                "top_n_flagged": TOP_N,
                "total_annual_revenue_at_risk_top_n": round(top["revenue_at_risk"].sum(), 2),
                "avg_churn_probability_top_n": round(top["churn_probability"].mean(), 3),
                "pct_top_n_month_to_month": round((top["Contract"] == "Month-to-month").mean() * 100, 1),
            }
        ]
    )
    summary.to_csv(OUT_SUMMARY, index=False)

    print(f"Held-out test AUC: {test_auc:.3f}")
    print(f"Held-out: overall churn {base_rate:.1%}; top-scored 10% actually churned at "
          f"{top_decile_rate:.1%} ({top_decile_rate / base_rate:.2f}x), capturing "
          f"{churners_captured:.1%} of all churners")
    print(f"Top {TOP_N} vs a random list of {TOP_N}: ${expected_at_risk:,.0f} vs "
          f"${random_list_at_risk:,.0f} expected at risk ({expected_at_risk / random_list_at_risk:.2f}x)")
    print(scenarios.to_string(index=False))
    print(f"Active customers scored: {len(active)}")
    print(f"Top {TOP_N} accounts represent ${top['revenue_at_risk'].sum():,.0f} in annualized revenue at risk")
    print(f"{summary['pct_top_n_month_to_month'].iloc[0]}% of the top {TOP_N} are on month-to-month contracts")
    print(f"\nSaved -> {OUT_RANKED}")
    print(f"Saved -> {OUT_SUMMARY}")


if __name__ == "__main__":
    main()

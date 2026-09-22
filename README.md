# Revenue-at-Risk Retention Analysis

**Which currently active customers are most likely to churn next, and how much
revenue is that worth — so a retention team knows exactly who to call first.**

Full write-up: [`memo/one_page_memo.md`](memo/one_page_memo.md) (2-minute read) or
[`Revenue_at_Risk_Case_Study.pdf`](Revenue_at_Risk_Case_Study.pdf) (detailed, downloadable case study)

## Headline result

- Trained and validated a churn model (held-out test **AUC 0.833**) on 7,032
  historical customer records.
- Scored the 5,163 currently active customers and ranked them by
  `churn probability × annualized revenue`.
- Found that customers on month-to-month contracts in their first year alone
  account for **49% of all annualized revenue lost to churn**.
- Flagged the top 150 active accounts, carrying **$114,608 in expected annualized
  revenue at risk** (probability-weighted; their actual combined billing is
  $167,537/year), for prioritized retention outreach.

*Note: this project uses IBM's public Telco Customer Churn dataset, framed as a
fictional company ("Meridian Communications") to turn it into a real business
decision rather than a data-exploration exercise. All numbers above are computed
from the real dataset, not fabricated.*

## What's in here

```
data/
  raw/telco_churn.csv              source data (IBM Telco Customer Churn, public)
  processed/                       cleaned data + model outputs (generated)
db/
  retention.db                     SQLite database (generated)
sql/
  01_schema.sql                    overall churn rate sanity check
  02_cohort_churn_rate.sql         churn rate & revenue exposure by cohort (CTE + window fn)
  03_sql_only_risk_heuristic.sql   rule-based risk ranking, no ML required (RANK() window fn)
scripts/
  01_clean_data.py                 clean the raw export, load into SQLite
  02_churn_drivers.py              logistic regression + chi-square significance tests
  03_revenue_at_risk.py            train/validate the model, score active customers, rank by $ risk
  04_make_charts.py                churn-rate charts for the memo
  05_build_case_study_pdf.py       generates the detailed PDF case study below
memo/
  one_page_memo.md                 the 2-minute-read deliverable — question, findings, recommendation
  assets/                          charts referenced in the memo and the case study
Revenue_at_Risk_Case_Study.pdf     detailed, systematic writeup — methodology, full driver table, limitations
retention_dashboard.pbix           the Power BI report (open in Power BI Desktop)
```

**Note:** there is no `.venv` folder in here on purpose — the Python environment
that runs these scripts lives outside this folder so it never clutters what you
see when you open it. See "How to reproduce" below.

## How to reproduce

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python scripts\01_clean_data.py
.venv\Scripts\python scripts\02_churn_drivers.py
.venv\Scripts\python scripts\03_revenue_at_risk.py
.venv\Scripts\python scripts\04_make_charts.py
```

## Stack

SQL (SQLite) · Python (pandas, statsmodels, scikit-learn) · Power BI

## Why two SQL approaches

[`03_sql_only_risk_heuristic.sql`](sql/03_sql_only_risk_heuristic.sql) deliberately
solves the same problem as the Python model, but with a rule-based score instead of
a trained model — useful context for a team without a data-science function, and a
concrete way to explain in an interview when you'd reach for one approach over the
other.

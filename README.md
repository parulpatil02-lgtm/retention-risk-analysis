# Revenue-at-Risk Retention Analysis

**Which active customers should a retention team call first, and what is calling them worth?**

Read the [one-page memo](memo/one_page_memo.md) (2 minutes) or the detailed
[case study PDF](Revenue_at_Risk_Case_Study.pdf).

## The business problem

A telecom provider's retention outreach is reactive and untargeted. Nobody can say
which active customers are likely to churn next or how much revenue that puts at
risk, so a limited retention budget is spent without a way to prioritize it.

## The data

IBM's public Telco Customer Churn dataset: 7,043 customer records (7,032 after
removing 11 brand-new accounts with no billing history) and 21 attributes -
tenure, contract type, services, payment method, monthly charges, churn outcome.
26.6% churned; 5,163 are still active. It is framed as a fictional company,
"Meridian Communications," to turn it into a real decision; every number is
computed from the real dataset.

## What I found

- **One cohort drives half the loss:** month-to-month customers in their first
  year are 28% of customers but **49% of all annualized revenue lost to churn**.
- **Ten variables significantly predict churn** (p < 0.001). A two-year contract
  cuts the odds of churn by ~73% versus month-to-month.
- **The top 150 active accounts carry $114,608 in expected annualized revenue at
  risk** (probability-weighted; their actual billing is $167,537/year). All 150 are
  month-to-month.

## What it changes

The decision: replace untargeted outreach with a ranked call list, leading with a
free tech-support or online-security add-on rather than a blanket discount.

| Evidence | Result | Basis |
|---|---|---|
| Churn among the model's top-scored 10% vs overall | **72.3% vs 26.6% (2.7x)** | Measured on held-out customers |
| Share of all real churners in that top 10% | **27.3%** (random would reach 10%) | Measured on held-out customers |
| Expected at-risk revenue, top 150 vs a random 150 | **$114.6K vs $23.8K (4.8x)** | Model-estimated |
| Revenue retained if an offer saves 10% / 20% / 30% | $11.5K / $22.9K / $34.4K a year | **Assumption - no campaign was run** |

The offer pays off only if it costs under $76 / $153 / $229 per contacted account at
those save rates. The last two rows are arithmetic on stated assumptions, not
results; the next step would be an A/B test to measure a real save rate.

## What's in here

```
data/
  raw/telco_churn.csv              source data (IBM Telco Customer Churn, public)
  processed/                       cleaned data, model outputs, ranked list, scenarios
db/
  retention.db                     SQLite database (generated)
sql/
  01_schema.sql                    overall churn rate sanity check
  02_cohort_churn_rate.sql         churn and revenue exposure by cohort (CTE + window function)
  03_sql_only_risk_heuristic.sql   rule-based risk ranking, no ML required (RANK())
scripts/
  01_clean_data.py                 clean the raw export, load into SQLite
  02_churn_drivers.py              logistic regression + chi-square significance tests
  03_revenue_at_risk.py            validate the model, score active customers, measure lift
  04_make_charts.py                charts for the memo
  05_build_case_study_pdf.py       generates the detailed PDF case study
memo/
  one_page_memo.md                 the decision memo
  assets/                          charts
Revenue_at_Risk_Case_Study.pdf     detailed writeup: methodology, driver table, limitations
retention_dashboard.pbix           the Power BI report (open in Power BI Desktop)
```

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

[`03_sql_only_risk_heuristic.sql`](sql/03_sql_only_risk_heuristic.sql) solves the same
ranking with a rule-based score instead of a trained model - useful for a team
without a data-science function, and a concrete way to explain when you'd reach for
one approach over the other.

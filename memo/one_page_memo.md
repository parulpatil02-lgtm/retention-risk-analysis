# Retention Memo — Who to Call First, and What It's Worth

**To:** VP of Customer Success, Meridian Communications *(fictional company — see note at the end)*
**From:** Analytics

## The business problem

Meridian's retention outreach is reactive and untargeted: there is no way to tell
which currently active customers are likely to churn next, or how much revenue that
puts at risk. So the team can't answer the two questions that decide where a
limited retention budget goes: *who should we call this month, and what is calling
them worth?*

## The data

IBM's public Telco Customer Churn dataset: 7,043 customer records (7,032 after
removing 11 brand-new accounts with no billing history), 21 attributes covering
tenure, contract type, services subscribed, payment method, monthly charges, and
whether the customer churned. **26.6%** of customers churned; **5,163** are still
active and are the ones worth scoring.

## What I found

- **One cohort drives half the loss.** Month-to-month customers in their first
  year are 1,994 of 7,032 customers (28%) but account for **49% of all annualized
  revenue lost to churn**.
- **Ten variables significantly predict churn (p < 0.001).** Longer contracts, tech
  support, online security and longer tenure are protective; electronic-check
  payment, fiber-optic internet, paperless billing and higher monthly charges raise
  risk. A two-year contract cuts the odds of churn by about 73% versus
  month-to-month, holding other factors constant.
- **The top 150 active accounts carry $114,608 in expected annualized revenue at
  risk** (churn probability weighted against revenue; their actual combined billing
  is $167,537/year). All 150 are on month-to-month contracts.

## What this changes

**The decision:** replace untargeted outreach with a ranked call list
(`data/processed/revenue_at_risk_ranked.csv`), and lead with a free 3-month
tech-support or online-security add-on — both are among the strongest protective
factors — rather than a blanket discount, which the driver analysis doesn't support.

**Measured, on held-out customers the model never saw:**
- The customers the model ranked in its top 10% actually churned at **72.3%**,
  versus **26.6%** overall — a **2.7x** lift.
- That 10% of customers contained **27.3% of all real churners**, against the 10%
  a random list would reach.

**Model-estimated:** the top-150 list carries **4.8x** the expected at-risk revenue
of a random list of 150 active customers ($114.6K vs $23.8K) — the same calls, aimed
at nearly five times the money.

**Illustrative — an assumption, not a result.** No retention campaign was run.
*If* the offer saves a share of the accounts expected to churn:

| Assumed save rate | Annual revenue retained | Offer pays off only if it costs less than |
|---|---|---|
| 10% | $11,461 | $76 per contacted account |
| 20% | $22,922 | $153 per contacted account |
| 30% | $34,382 | $229 per contacted account |

## Approach

Logistic regression on the 7,032 historical customers, validated on a held-out 20%
(**AUC 0.833**), refit on all history, then applied only to the 5,163 active
accounts. Each is scored as `churn probability × annualized revenue`
(monthly charge × 12) and ranked.

## Assumptions & limitations

- Active customers also appear in the training data labeled as "retained," although
  their future is unknown — a standard simplification with snapshot data. A
  time-based split would be a stronger design.
- Nothing here has been validated against the outcome of a real campaign; test the
  offer on a subset first.
- Revenue at risk uses each customer's current monthly rate, ignoring future price
  changes, upgrades or downgrades.
- The scenario table is arithmetic on stated assumptions, not a forecast.

## What I'd want next

A/B test the add-on offer against a no-offer control on part of the ranked list, to
replace the assumed save rates with a measured one, and re-score monthly.

---
*The data is IBM's public Telco Customer Churn dataset. "Meridian Communications" is
a fictional framing to make this a real retention decision rather than a
data-exploration exercise; every figure above is computed from the dataset.*

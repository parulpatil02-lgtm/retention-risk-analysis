# Retention Memo — Revenue at Risk, Q-over-Q

**To:** VP of Customer Success, Meridian Communications *(fictional company — see note below)*
**From:** Analytics
**Re:** Which active accounts are worth a retention call this month, and why

## The question

Meridian doesn't have a way to tell which currently active customers are likely to
churn next, or how much revenue that represents — retention outreach today is
reactive, not prioritized. This memo answers: *who should we call first, and what's
the dollar case for calling them?*

## Approach

Trained a logistic regression on 7,032 historical customer records (26.6% overall
churn rate) using tenure, contract type, internet service, add-ons, billing method,
and monthly spend. Validated on a held-out 20% test set (**AUC 0.833** — the model
meaningfully separates churners from non-churners, not just noise). Applied the
trained model only to the **5,163 currently active** accounts to score forward-looking
risk, then ranked them by `churn probability × annualized revenue`.

## Key findings

- **Contract type dominates everything else.** Month-to-month customers in their
  first year account for **49% of all annualized revenue lost to churn**, despite
  being a minority of the customer base (1,994 of 7,032). This single cohort is the
  highest-leverage place to act.
- **Ten variables are statistically significant churn predictors (p < 0.001), and
  they split cleanly into protective vs. risk-increasing.** Longer contracts, having
  tech support, having online security, and longer tenure are all strongly
  *protective*. Paying by electronic check, having fiber-optic internet, higher
  monthly charges, and paperless billing all *increase* risk. Contract length has
  the largest effect by far: a two-year contract reduces the odds of churn by about
  73% relative to a month-to-month customer, holding everything else constant.
- **The top 150 at-risk active accounts represent $114,608 in annualized revenue**,
  and every one of them is on a month-to-month contract — the model isn't just
  confirming what we already suspected about contract type, it's telling us exactly
  *which* month-to-month accounts to prioritize by dollar value, not just by risk.

## Recommendation

Route the top 150 ranked accounts (`revenue_at_risk_ranked.csv`) to retention outreach
this month, prioritized by the `revenue_at_risk` column. Bundling a free 3-month
tech-support or online-security add-on for this segment is the most defensible first
offer to test, since both are among the strongest protective factors in the model —
not a blanket discount.

## Assumptions & limitations

- Customers with zero tenure (11 records) were excluded — they have no billing
  history and can't yet be scored for churn risk.
- The model was trained on historical customers, including those who already
  churned, then applied only to currently active accounts — it has not been
  validated against actual outcomes of a real retention campaign, so the offer
  above should be tested on a subset first, not rolled out wholesale.
- Revenue at risk is annualized at the *current* monthly rate; it does not account
  for future price changes or plan upgrades/downgrades.

## What I'd want next

A/B test the tech-support/online-security offer against a no-offer control group
on a sample of the ranked list, and re-score monthly rather than as a one-time list.

---
*Note on the data: this uses IBM's public Telco Customer Churn dataset. "Meridian
Communications" is a fictional framing built on top of it to structure this as a
real retention decision rather than a data-exploration exercise — the numbers above
are genuinely computed from the dataset, not fabricated.*

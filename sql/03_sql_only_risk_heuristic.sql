-- A SQL-only fallback risk ranking, for a team without a data-science
-- function or a Python model available. It flags the same well-known
-- red flags the logistic regression later confirms are significant
-- (month-to-month contract, no tech support, electronic check payment,
-- low tenure) and ranks currently active customers with RANK().
-- This is intentionally a simpler, rule-based alternative to the
-- probability-based model in /scripts/03_revenue_at_risk.py -- worth
-- having both, and worth being able to explain when you'd reach for
-- which one.

WITH scored AS (
    SELECT
        customerID,
        Contract,
        InternetService,
        tenure,
        MonthlyCharges,
        (CASE WHEN Contract = 'Month-to-month' THEN 2 ELSE 0 END) +
        (CASE WHEN TechSupport = 'No' THEN 1 ELSE 0 END) +
        (CASE WHEN OnlineSecurity = 'No' THEN 1 ELSE 0 END) +
        (CASE WHEN PaymentMethod = 'Electronic check' THEN 1 ELSE 0 END) +
        (CASE WHEN tenure <= 12 THEN 2 ELSE 0 END)
                                                    AS risk_flags,
        MonthlyCharges * 12                        AS annual_revenue
    FROM customers
    WHERE Churn = 'No'   -- only currently active customers can be "at risk"
)
SELECT
    customerID,
    Contract,
    InternetService,
    tenure,
    MonthlyCharges,
    annual_revenue,
    risk_flags,
    RANK() OVER (ORDER BY risk_flags DESC, annual_revenue DESC) AS risk_rank
FROM scored
ORDER BY risk_rank
LIMIT 150;

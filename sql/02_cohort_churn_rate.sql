-- Churn rate and revenue exposure by tenure cohort and contract type.
-- Uses a CTE to pre-aggregate, then a window function to add each
-- cohort's share of total churned revenue -- the kind of "how big a
-- problem is this slice" framing a retention lead actually asks for.

WITH cohort AS (
    SELECT
        TenureBucket,
        Contract,
        COUNT(*)                                   AS customers,
        SUM(ChurnFlag)                              AS churned,
        ROUND(100.0 * SUM(ChurnFlag) / COUNT(*), 1) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 0)
                                                     AS annual_revenue_lost
    FROM customers
    GROUP BY TenureBucket, Contract
)
SELECT
    TenureBucket,
    Contract,
    customers,
    churned,
    churn_rate_pct,
    annual_revenue_lost,
    ROUND(
        100.0 * annual_revenue_lost / SUM(annual_revenue_lost) OVER (),
        1
    ) AS pct_of_total_revenue_lost
FROM cohort
ORDER BY annual_revenue_lost DESC;

-- Schema note: the source export from Meridian Communications' billing
-- system is a single flat customer table (this is normal for an ops/billing
-- export — it isn't already modeled as a star schema). The queries below
-- build the structure (cohorts, risk ranking) on top of it rather than
-- pretending the raw export was already relational.

-- customers(
--   customerID TEXT PRIMARY KEY,
--   gender TEXT, SeniorCitizen TEXT, Partner TEXT, Dependents TEXT,
--   tenure INTEGER, PhoneService TEXT, MultipleLines TEXT,
--   InternetService TEXT, OnlineSecurity TEXT, OnlineBackup TEXT,
--   DeviceProtection TEXT, TechSupport TEXT, StreamingTV TEXT,
--   StreamingMovies TEXT, Contract TEXT, PaperlessBilling TEXT,
--   PaymentMethod TEXT, MonthlyCharges REAL, TotalCharges REAL,
--   Churn TEXT, ChurnFlag INTEGER, TenureBucket TEXT
-- )

SELECT COUNT(*) AS total_customers,
       SUM(ChurnFlag) AS churned_customers,
       ROUND(100.0 * SUM(ChurnFlag) / COUNT(*), 1) AS churn_rate_pct
FROM customers;

# Power BI build guide (first-time-user version)

This is the one manual step in the whole project. Power BI Desktop is a Windows
GUI app with no scripting interface, so this is a real click-by-click walkthrough.
Budget about an hour.

## 0. Install and open

1. Search **"Power BI Desktop"** in the Microsoft Store and install it (it's free).
   The Store version auto-updates, which is preferable to the standalone installer.
2. Launch it. A welcome screen may pop up asking you to sign in — **skip that for
   now** (click the X or "Get started"). You don't need an account to build the
   report locally, only to publish it at the very end.

## 1. Import the data

1. On the **Home** ribbon (top of the window), click **Get Data**.
2. Choose **Text/CSV** from the list.
3. Navigate to this project's `data/processed/customers_clean.csv` and select it.
4. A preview window appears showing the table. Click **Load** (not "Transform
   Data" — the data's already clean).
5. Repeat steps 1–4 for `data/processed/revenue_at_risk_ranked.csv`.
6. On the right edge of the window, the **Fields** pane now lists both tables.

## 2. Build the data model

1. On the far-left sidebar, click the **Model view** icon (three connected boxes
   — it's usually the third icon down).
2. You'll see two boxes, one per table, each listing its columns.
3. Find `customerID` in the `customers_clean` box, click and hold it, and drag it
   onto `customerID` in the `revenue_at_risk_ranked` box. Release — a line now
   connects the two tables.
4. Double-click that line to confirm: cardinality **"One to one"**, cross-filter
   direction **"Both"**. Click OK.

This is what makes it a real data model instead of one flat table — worth saying
out loud in an interview.

## 3. Add the measures

1. Go back to **Report view** (top icon in the left sidebar).
2. In the Fields pane, right-click the `customers_clean` table → **New measure**.
3. A formula bar opens at the top of the canvas. Type exactly:
   ```
   Overall Churn Rate = DIVIDE(SUM(customers_clean[ChurnFlag]), COUNTROWS(customers_clean))
   ```
   Press Enter.
4. Repeat (right-click `customers_clean` → New measure) for:
   ```
   Total Active Customers = COUNTROWS(customers_clean)
   ```
5. Right-click `revenue_at_risk_ranked` → New measure, add:
   ```
   Total Revenue at Risk (Top 150) = SUM(revenue_at_risk_ranked[revenue_at_risk])
   Avg Churn Probability (Top 150) = AVERAGE(revenue_at_risk_ranked[churn_probability])
   ```

**Why "Overall Churn Rate" does double duty:** a measure isn't a fixed number —
it recalculates based on whatever it's charted against. Drop it on a KPI card and
it shows the overall rate; drop it in a bar chart with `Contract` on the axis and
it automatically shows the rate *per contract type*. You don't need a separate
measure for every breakdown.

## 4. Page 1 — Executive summary

1. Right-click the "Page 1" tab at the bottom → **Rename** → `Executive Summary`.
2. In the **Visualizations** pane (right side), click the **Card** icon. An empty
   card appears — drag `Overall Churn Rate` from the Fields pane onto it (or
   check its box while the card is selected).
3. Add two more cards the same way for `Total Revenue at Risk (Top 150)` and
   `Avg Churn Probability (Top 150)`. Drag them into a row along the top.
4. Click the **Clustered Column Chart** icon → drag `Contract` into the **X-axis**
   well and `Overall Churn Rate` into the **Y-axis** well.
5. Add a second clustered column chart the same way, using `TenureBucket` on the
   X-axis instead.
6. Insert ribbon → **Text box** → add: *"Month-to-month customers in their first
   year drive 49% of all revenue lost to churn."*

## 5. Page 2 — Drill-down / call list

1. Click the **+** tab at the bottom to add a page → rename it `Call List`.
2. Click the **Table** icon in Visualizations. Drag these fields from
   `revenue_at_risk_ranked` into the Columns well, in this order: `risk_rank`,
   `customerID`, `Contract`, `InternetService`, `tenure`, `MonthlyCharges`,
   `churn_probability`, `revenue_at_risk`.
3. Click the `risk_rank` column header in the table to sort ascending.
4. Click the **Slicer** icon, drag it onto the canvas, assign field `Contract`.
   Add a second slicer for `InternetService`.
5. Click the table visual, then the paint-roller **Format your visual** icon →
   find **Cell elements** → turn on formatting for `revenue_at_risk` → choose
   **Background color**, set it to a color scale (light for low, dark teal for
   high) → Apply.

## 6. Save

`Ctrl+S` → save as `retention_dashboard.pbix` inside this `powerbi/` folder, so
it's part of the project.

## 7. Publish

1. Home ribbon → **Publish**.
2. Sign in if prompted. **Try your ASU email first** — many universities include
   a free Power BI Pro license through Microsoft 365 Education, which just works.
3. Choose **My workspace** as the destination and wait for it to finish.
4. Click the link in the completion dialog, or go to **app.powerbi.com**, sign
   in, and find the report under **My workspace**.

## 8. Get a public shareable link

1. With the report open in the Power BI service (not Desktop), go to
   **File → Embed report → Publish to web (public)**.
2. A warning appears saying this makes the report visible to *anyone with the
   link, no login required*. That's expected and fine here — this project only
   uses IBM's public, anonymized Telco dataset, no real personal data. Confirm.
3. Copy the generated link — that's what goes on your resume and portfolio.

**If "Publish to web" is greyed out or blocked** (some university tenants disable
it by admin policy): sign up for a separate free personal Microsoft account
(outlook.com) just for this, sign into Power BI with that instead, and republish
from there — personal accounts don't have that restriction.

## 9. Backup

Take a screenshot of both pages (`Win+Shift+S`) and save them alongside this
project, in case the live link ever breaks and you need a static fallback for
your portfolio card.

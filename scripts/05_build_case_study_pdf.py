"""
Builds a polished, multi-page PDF case study of the retention analysis --
a systematic, detailed writeup meant to be downloaded and shared directly
(attached to an application, sent to a recruiter), separate from the
one-page memo which is optimized for a two-minute read.
"""
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    CondPageBreak,
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "memo" / "assets"
OUT_PATH = ROOT / "Revenue_at_Risk_Case_Study.pdf"

TEAL = colors.HexColor("#1F6F5C")
TEAL_DARK = colors.HexColor("#0F4438")
TEAL_SOFT = colors.HexColor("#E3EFE9")
INK = colors.HexColor("#1B211D")
INK_SOFT = colors.HexColor("#4E594F")
BORDER = colors.HexColor("#D7DACC")
WARN_SOFT = colors.HexColor("#F4E6D6")
WARN_DARK = colors.HexColor("#8A4A15")

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, leading=26, textColor=TEAL_DARK, spaceAfter=4,
)
subtitle_style = ParagraphStyle(
    "SubtitleCustom", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=12, leading=16, textColor=INK_SOFT, spaceAfter=2,
)
meta_style = ParagraphStyle(
    "MetaCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9, leading=12, textColor=INK_SOFT, spaceAfter=14,
)
h2_style = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=14, leading=18, textColor=TEAL_DARK, spaceBefore=18, spaceAfter=8, keepWithNext=1,
)
h3_style = ParagraphStyle(
    "H3Custom", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=11, leading=14, textColor=INK, spaceBefore=10, spaceAfter=4, keepWithNext=1,
)
body_style = ParagraphStyle(
    "BodyCustom", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=15, textColor=INK, spaceAfter=8,
)
body_bold = ParagraphStyle(
    "BodyBold", parent=body_style, fontName="Helvetica-Bold",
)
caption_style = ParagraphStyle(
    "CaptionCustom", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=8.5, leading=11, textColor=INK_SOFT, alignment=1, spaceAfter=4,
)
list_style = ParagraphStyle(
    "ListCustom", parent=body_style, spaceAfter=4,
)


def stat_box(value, label):
    return Table(
        [[Paragraph(f'<font color="#0F4438" size="15"><b>{value}</b></font>', body_style)],
         [Paragraph(f'<font color="#4E594F" size="7.5">{label}</font>', body_style)]],
        colWidths=[1.55 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("TOPPADDING", (0, 1), (-1, 1), 2),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]),
    )


def callout(text, accent=TEAL, bg=TEAL_SOFT):
    return Table(
        [[Paragraph(text, body_style)]],
        colWidths=[6.5 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]),
    )


def build():
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=LETTER,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        title="Revenue-at-Risk Retention Analysis - Case Study",
        author="Parul Patil",
    )

    story = []

    # ---------- Header ----------
    story.append(Paragraph("Revenue-at-Risk Retention Analysis", title_style))
    story.append(Paragraph("A Case Study in Churn Prediction &amp; Business Decision-Making", subtitle_style))
    story.append(Paragraph(
        "Parul Patil &nbsp;·&nbsp; September 2026 &nbsp;·&nbsp; "
        '<a href="https://github.com/parulpatil02-lgtm/retention-risk-analysis" color="#0F4438">'
        "github.com/parulpatil02-lgtm/retention-risk-analysis</a>",
        meta_style,
    ))

    story.append(callout(
        "<b>The question:</b> which currently active customers are most likely to churn next, "
        "and how much revenue does that represent - so a retention team knows exactly who to "
        "call first, and can defend the dollar case for doing it.", TEAL, TEAL_SOFT,
    ))
    story.append(Spacer(1, 12))

    stats_row = Table(
        [[stat_box("7,032", "historical customers analyzed"),
          stat_box("0.833", "held-out test AUC"),
          stat_box("$114.6K", "expected revenue at risk, top 150 accounts"),
          stat_box("49%", "of revenue lost to churn from one cohort")]],
        colWidths=[1.6 * inch] * 4,
        style=TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]),
    )
    story.append(stats_row)

    # ---------- Executive Summary ----------
    story.append(Paragraph("1. Executive Summary", h2_style))
    story.append(Paragraph(
        "Retention outreach at Meridian Communications <i>(a fictional company built on real, "
        "public data - see the Data section)</i> was reactive rather than prioritized: there was "
        "no systematic way to identify which active customers were most likely to churn, or how "
        "much revenue was actually on the line. This project builds that system end to end: a "
        "validated statistical model of churn drivers, a forward-looking risk score applied only "
        "to currently active accounts, and a dollar-ranked call list a retention team could act "
        "on immediately.", body_style,
    ))
    story.append(Paragraph(
        "The single biggest finding: <b>customers on month-to-month contracts in their first year "
        "account for 49% of all annualized revenue lost to churn</b>, despite being a minority of "
        "the customer base. The top 150 currently active accounts ranked by the model carry "
        "$114,608 in expected annualized revenue at risk. On customers the model never saw, the "
        "accounts it ranked in its top 10% actually churned at 72.3% versus 26.6% overall - a "
        "2.7x lift - which is what makes the ranked list worth acting on.", body_style,
    ))

    # ---------- Business Context ----------
    story.append(Paragraph("2. Business Context", h2_style))
    story.append(Paragraph(
        "A subscription telecom/internet provider loses revenue every time a customer churns, "
        "but not every churned customer is equally costly, and not every active customer is "
        "equally at risk. Without a model, retention teams either contact everyone (expensive, "
        "low signal) or rely on gut feel about which segments are risky (imprecise, not "
        "dollar-weighted). The goal here is a specific, defensible answer to two questions a VP "
        "of Customer Success would actually ask: <i>who should we call this month, and what's the "
        "dollar case for calling them instead of someone else?</i>", body_style,
    ))

    # ---------- Data ----------
    story.append(Paragraph("3. Data", h2_style))
    story.append(Paragraph(
        "The analysis uses IBM's public Telco Customer Churn dataset (7,043 customers, 21 "
        "attributes covering tenure, contract type, services subscribed, billing method, and "
        "churn outcome). It is framed here as a fictional company, “Meridian Communications,” "
        "to structure the work as a real retention decision rather than a data-exploration "
        "exercise - every number in this document is computed from the real dataset, not "
        "fabricated.", body_style,
    ))

    # ---------- Methodology ----------
    story.append(Paragraph("4. Methodology", h2_style))

    story.append(Paragraph("4.1 &nbsp; Data Cleaning", h3_style))
    story.append(ListFlowable([
        ListItem(Paragraph(
            "Excluded 11 customers with zero tenure - they have no billing history yet and "
            "cannot meaningfully be scored for churn risk.", list_style)),
        ListItem(Paragraph(
            "Collapsed the “No internet service” category (present in six add-on columns: "
            "online security, backup, device protection, tech support, streaming TV/movies) into "
            "“No.” Left uncollapsed, this category is perfectly collinear with "
            "<i>InternetService = No</i> and produces a singular matrix in logistic regression - "
            "a real bug encountered and fixed during this analysis, not a hypothetical.", list_style)),
        ListItem(Paragraph(
            "Bucketed tenure into four cohorts (0–12, 13–24, 25–48, 49–72 months) for "
            "cohort-level reporting.", list_style)),
    ], bulletType="bullet", start="circle"))

    story.append(Paragraph("4.2 &nbsp; Statistical Testing", h3_style))
    story.append(Paragraph(
        "Chi-square tests of independence were run for eight categorical variables against churn "
        "(Contract, InternetService, TechSupport, OnlineSecurity, PaperlessBilling, PaymentMethod, "
        "SeniorCitizen, Dependents). All eight are significant at p &lt; 0.001, confirming they are "
        "not independent of churn before any modeling assumptions are introduced.", body_style,
    ))

    story.append(Paragraph("4.3 &nbsp; Predictive Modeling", h3_style))
    story.append(Paragraph(
        "A logistic regression was fit on the full historical dataset (tenure, monthly charges, "
        "contract, internet service, tech support, online security, paperless billing, payment "
        "method, senior citizen status, dependents) to identify which factors drive churn and in "
        "which direction, with p-values for statistical significance. Separately, a "
        "scikit-learn logistic regression was trained on an 80/20 train/test split for the "
        "prediction task itself, and evaluated on the held-out 20% - achieving an "
        "<b>AUC of 0.833</b>, meaning the model meaningfully separates churners from "
        "non-churners rather than performing close to chance (0.5).", body_style,
    ))

    story.append(Paragraph("4.4 &nbsp; Scoring &amp; Ranking", h3_style))
    story.append(Paragraph(
        "The model was refit on the complete historical dataset, then applied only to the 5,163 "
        "<b>currently active</b> customers - a customer who has already churned does not need a "
        "future-risk prediction. Each active customer was scored with: "
        "<i>expected revenue at risk = churn probability × annualized revenue</i> "
        "(monthly charge × 12). This is a probability-weighted expected value, not a customer's "
        "actual billing - a distinction worth stating explicitly, since it changes how the top-line "
        "dollar figure should be interpreted (see Section 5.3).", body_style,
    ))

    story.append(PageBreak())

    # ---------- Findings ----------
    story.append(Paragraph("5. Findings", h2_style))

    story.append(Paragraph("5.1 &nbsp; What Actually Drives Churn", h3_style))
    story.append(Paragraph(
        "Ten variables are statistically significant churn predictors at p &lt; 0.001. They split "
        "cleanly into protective and risk-increasing factors:", body_style,
    ))

    driver_data = [
        ["Factor", "Effect", "Odds Ratio", "p-value"],
        ["Two-year contract (vs. month-to-month)", "Protective", "0.267", "< 0.001"],
        ["One-year contract (vs. month-to-month)", "Protective", "0.518", "< 0.001"],
        ["Longer tenure (per month)", "Protective", "0.969", "< 0.001"],
        ["Has online security add-on", "Protective", "0.635", "< 0.001"],
        ["Has tech support add-on", "Protective", "0.679", "< 0.001"],
        ["No internet service", "Protective", "0.465", "< 0.001"],
        ["Fiber-optic internet", "Increases risk", "1.658", "< 0.001"],
        ["Pays by electronic check", "Increases risk", "1.431", "< 0.001"],
        ["Paperless billing", "Increases risk", "1.449", "< 0.001"],
        ["Higher monthly charges (per $)", "Increases risk", "1.011", "< 0.001"],
    ]
    driver_table = Table(driver_data, colWidths=[2.7 * inch, 1.15 * inch, 1.0 * inch, 0.85 * inch])
    driver_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TEAL_SOFT]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (2, 0), (3, -1), "CENTER"),
    ]))
    story.append(driver_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Contract length has the largest effect of any categorical driver: moving from a "
        "month-to-month to a two-year contract reduces the odds of churn by roughly 73%, holding "
        "other factors constant. Two secondary signals were also significant at a weaker threshold "
        "(p &lt; 0.05): having dependents is mildly protective (OR 0.838), and being a senior "
        "citizen mildly increases risk (OR 1.286).", body_style,
    ))

    story.append(Paragraph("5.2 &nbsp; Where the Charts Confirm the Story", h3_style))
    img1 = Image(str(ASSETS / "churn_by_contract.png"), width=2.95 * inch, height=1.72 * inch)
    img2 = Image(str(ASSETS / "churn_by_tenure.png"), width=2.95 * inch, height=1.72 * inch)
    chart_row = Table([[img1, img2]], colWidths=[3.15 * inch, 3.15 * inch])
    chart_row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(chart_row)
    story.append(Paragraph(
        "Churn falls from 42.7% (month-to-month) to 2.8% (two-year contracts), and from 47.7% in "
        "a customer's first year to 9.5% after four years - both consistent with the regression's "
        "conclusions above, not just the raw correlations behind them.", caption_style,
    ))

    story.append(Paragraph("5.3 &nbsp; The Concentration Finding", h3_style))
    story.append(callout(
        "New, month-to-month customers (0–12 months tenure) are 1,994 of the 7,032 total "
        "customers (28%) - but they account for <b>49.1% of all annualized revenue lost to churn</b> "
        "($819,617 of the total). This single cohort is the highest-leverage place to intervene.",
        TEAL, TEAL_SOFT,
    ))

    story.append(Paragraph("5.4 &nbsp; The Ranked Call List", h3_style))
    story.append(Paragraph(
        "Scoring the 5,163 active customers and ranking by expected revenue at risk surfaces the "
        "top 150 accounts to prioritize. A precise reading of the dollar figure matters here: "
        "these 150 accounts carry <b>$114,608 in expected annualized revenue at risk</b> "
        "(their churn probability weighted against their revenue). Their actual combined billing "
        "is higher - <b>$167,537/year</b> - but not all of that is expected to be lost; $114,608 is "
        "the risk-adjusted figure a retention budget should be sized against. Notably, "
        "<b>100% of the top 150 are on month-to-month contracts</b>, which is not a coincidence "
        "given the driver analysis above - it is the model converging on the same conclusion from "
        "a different angle.", body_style,
    ))

    # ---------- Recommendation & impact ----------
    story.append(Paragraph("6. Recommendation &amp; What It Changes", h2_style))
    story.append(callout(
        "Replace untargeted outreach with the ranked call list: route the top 150 accounts to "
        "retention this month, and lead with a free 3-month tech-support or online-security "
        "add-on - both are among the strongest statistically significant protective factors - "
        "rather than a blanket discount, which the driver analysis does not support.",
        WARN_DARK, WARN_SOFT,
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The evidence for the change, separated by how much each piece can be trusted:", body_style))

    s = pd.read_csv(ROOT / "data" / "processed" / "revenue_at_risk_summary.csv").iloc[0]
    sc = pd.read_csv(ROOT / "data" / "processed" / "impact_scenarios.csv")
    evidence = [["Evidence", "Result", "Basis"],
        ["Churn in the model's top-scored 10% vs overall",
         f"{s.held_out_top_decile_churn_rate:.1%} vs {s.held_out_base_churn_rate:.1%} "
         f"({s.held_out_top_decile_lift:.1f}x)", "Measured, held-out customers"],
        ["Share of all real churners in that top 10%",
         f"{s.held_out_churners_in_top_decile:.1%} (random: 10%)", "Measured, held-out customers"],
        ["Expected at-risk revenue, top 150 vs a random 150",
         f"${s.total_annual_revenue_at_risk_top_n / 1000:,.1f}K vs "
         f"${s.expected_at_risk_random_list_same_size / 1000:,.1f}K "
         f"({s.targeting_advantage_vs_random:.1f}x)", "Model-estimated"]]
    for r in sc.itertuples():
        evidence.append([
            f"Revenue retained if the offer saves {r.assumed_save_rate:.0%}",
            f"${r.annual_revenue_retained:,.0f}/yr; offer must cost < "
            f"${r.breakeven_offer_cost_per_account:,.0f}/account", "Assumption, not a result"])
    cell = ParagraphStyle("Cell", parent=body_style, fontSize=8.5, leading=11, spaceAfter=0)
    head = ParagraphStyle("CellHead", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
    evidence = [[Paragraph(c, head if i == 0 else cell) for c in row]  # wrapped so long text can't overflow
                for i, row in enumerate(evidence)]
    ev_table = Table(evidence, colWidths=[2.45 * inch, 2.3 * inch, 1.75 * inch])
    ev_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TEAL_SOFT]),
        ("BACKGROUND", (0, 4), (-1, -1), WARN_SOFT),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ev_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "No retention campaign was run, so the shaded rows are arithmetic on stated assumptions, "
        "not outcomes. Replacing them with a measured save rate is the point of the A/B test "
        "proposed below.", caption_style))

    # ---------- Limitations ----------
    story.append(CondPageBreak(1.6 * inch))  # a list can split, so keepWithNext alone won't hold the heading
    story.append(Paragraph("7. Assumptions &amp; Limitations", h2_style))
    story.append(ListFlowable([
        ListItem(Paragraph(
            "The model was trained on historical outcomes (including customers who already "
            "churned) and then applied to active accounts going forward - it has not yet been "
            "validated against the actual outcome of a real retention campaign. The recommended "
            "offer should be tested on a subset before a full rollout.", list_style)),
        ListItem(Paragraph(
            "Active customers also appear in the training data labeled as “retained,” although "
            "their future is unknown - a standard simplification with snapshot data. A time-based "
            "split would be a stronger design.", list_style)),
        ListItem(Paragraph(
            "Revenue at risk is annualized at the customer's <i>current</i> monthly rate; it does "
            "not account for future price changes, upgrades, or downgrades.", list_style)),
        ListItem(Paragraph(
            "Collapsing “No internet service” into “No” for add-on columns removes exact "
            "multicollinearity, but a partial correlation remains between InternetService and the "
            "add-on columns - coefficients for those add-ons should be read as “effect among "
            "customers with comparable internet service,” not fully independent effects.", list_style)),
    ], bulletType="bullet", start="circle"))

    # ---------- Technical appendix ----------
    story.append(Paragraph("8. Technical Appendix", h2_style))
    story.append(Paragraph("<b>Stack:</b> SQL (SQLite) &middot; Python (pandas, statsmodels, scikit-learn) &middot; Power BI", body_style))
    story.append(Paragraph(
        "<b>Two SQL approaches, deliberately:</b> alongside the Python model, a pure-SQL "
        "rule-based risk heuristic (window functions, no ML dependency) solves the same ranking "
        "problem for a team without a data-science function - useful context for explaining when "
        "each approach is the right tool.", body_style,
    ))
    story.append(Paragraph(
        "<b>Full code, data, and the interactive Power BI dashboard:</b> "
        '<a href="https://github.com/parulpatil02-lgtm/retention-risk-analysis" color="#0F4438">'
        "github.com/parulpatil02-lgtm/retention-risk-analysis</a>", body_style,
    ))

    doc.build(story)
    print(f"Saved -> {OUT_PATH}")


if __name__ == "__main__":
    build()

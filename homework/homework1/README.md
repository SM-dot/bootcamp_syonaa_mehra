# News Sentiment Impact on Stocks
**Stage:** Problem Framing & Scoping (Stage 01)
## Problem Statement
The problem is to quantify the immediate impact of major news events on the stock prices of technology companies. In a highly automated trading environment, news and sentiment can drive rapid price movements. Understanding this relationship is critical for developing more robust trading strategies that account for these external shocks, rather than just historical price data.
## Stakeholder & User
The primary stakeholder is a Quantitative Researcher or Portfolio. They are the decision-makers who would use the findings to refine trading models and risk management strategies. The end user of the output would be a Junior Trader who needs a clear, actionable signal or metric to inform their daily trading activities. The context is fast-paced, so the answer must be timely and easily interpretable.

## Useful Answer & Decision
The most useful answer would be causal and predictive. We want to determine if a specific type of news (e.g., a positive earnings report vs. a negative product recall) causes a measurable price movement and, if so, to what degree. The deliverable would be a metric (e.g., a "sentiment-volatility index") or an artifact like a visualization or a summary table that shows the average price change within a 15-minute window following a specific type of news event. This information would allow the quant researcher to make a decision about whether to integrate news sentiment into a new trading strategy or as an alert for risk management.


## Assumptions & Constraints
* **Data Availability:** Assume access to a historical dataset of news headlines and corresponding stock prices for a defined period.
* **Capacity:** This analysis will be scoped to a small basket of tech and healthcare stocks to be feasible.

## Known Unknowns / Risks
* **Sentiment Accuracy:** The accuracy of public sentiment analysis tools can be variable. I'll need to define clear sentiment categories (positive, negative, neutral) and document their limitations.
* **Causality vs. Correlation:** It may be difficult to definitively prove a causal link. I will need to be careful with the framing of my conclusions and identify other potential confounding variables. I will address this by focusing on event-driven analysis rather than simple correlation.

## Lifecycle Mapping
- Map problem to business need → Problem Framing & Scoping (Stage 01) → Scoping paragraph & README
- Analyze news and stock data → Data Collection & Cleaning (Stage 02) → Cleaned CSVs in `/data/` and basic EDA notebook
- Model sentiment impact → Modeling & Analysis (Stage 03) → Predictive model notebook
- Present findings to stakeholder → Communication & Presentation (Stage 04) → Stakeholder memo and final slide deck

## Repo Plan
The repo will contain: `/data/` for raw data, `/src/` for Python scripts, `/notebooks/` for Jupyter notebooks, and `/docs/` for project documentation. I plan to commit updates daily as I progress through the assignment.

# Trade Signal Generator

**Stage:** Problem Framing & Scoping (Stage 01)

---

## Problem Statement
In algorithmic trading, generating reliable trade signals (e.g., predictions of stock price movements based on momentum or volume patterns) is essential for capturing profitable opportunities, but poor signals lead to inconsistent returns or losses. This project aims to develop a tool to generate a predictive trade signal for a single stock, using historical market data to forecast short-term price direction (up or down) with an associated confidence score. By creating actionable signals, the tool will enable algorithm developers to build more effective trading strategies in dynamic markets.

---

## Stakeholder & User
- **Stakeholder:** The trading firm’s strategy team, responsible for developing high-performing algorithmic trading systems.
- **User:** Algorithm developers at the trading firm, who use the tool during strategy prototyping to generate and test new signals. The tool integrates into their Python-based workflow, providing signals within their existing development environment.

---

## Useful Answer & Decision
- **Type:** Predictive
- **Metric:** Signal confidence score (probability of correct price direction prediction, e.g., 0-1 scale).
- **Artifact:** A generated signal output (e.g., "Buy AAPL with 0.75 confidence") and a report on signal generation logic, enabling developers to incorporate signals into trading algorithms.

---

## Assumptions & Constraints
- **Data Availability:** Public tick-level market data (e.g., Alpaca or Yahoo Finance APIs) is accessible for a single stock (e.g., AAPL).
- **Capacity:** Signal generation is limited to one stock and simple patterns (e.g., momentum) to ensure feasibility.
- **Latency:** Analysis is offline at this stage, using historical tick data to prototype signal generation.
- **Compliance:** All data is publicly available, avoiding proprietary or restricted datasets.

---

## Known Unknowns / Risks
- **Data Quality:** Public tick data may include noise or gaps, affecting signal accuracy. **Mitigation:** Clean data and validate with multiple sources.
- **Market Predictability:** Signals may perform poorly in unpredictable markets (e.g., high volatility). **Mitigation:** Test signals across different market conditions.
- **Overfitting:** Simple models might fit historical data too closely without generalizing. **Mitigation:** Use cross-validation techniques in prototyping.

---

## Lifecycle Mapping
| Goal | Stage | Deliverable |
|---|---|---|
| Map problem to business need | Problem Framing & Scoping (Stage 01) | Scoping paragraph, README, stakeholder memo |
| Collect and process tick data | Data Collection & Cleaning (Stage 02) | Cleaned tick data CSVs in `/data/`, exploratory data analysis notebook |
| Develop signal generation model | Analysis (Stage 03) | Python script for signal generation |
| Communicate and refine | Communication (Stage 04) | Final report and signal visualization mockup |

---

## Data Storage 
This project acquires historical and real-time data for the top 10 performing stocks. We use the yfinance library to programmatically pull data from Yahoo Finance.

Data Description

Historical Data: We've collected the past five years of daily OHLCV (Open, High, Low, Close, Volume) data for each stock. This raw data is stored in two formats to support different analysis needs:

 - Single Combined File: All historical data for the 10 stocks is saved in a single, long-format CSV file (top10_historical_...csv). This format is ideal for group analysis, cross-stock comparisons, and training machine learning models.

 - Separate Files: Individual CSV files are created for each stock (e.g., aapl_historical_...csv). This format is useful for in-depth, single-stock analysis.

Reproducibility: 
To ensure data reproducibility, all saved files are automatically named with a timestamp (YYYY-MM-DD_HH-MM-SS). This creates a versioned snapshot of the raw data at the time of acquisition.

# Outlier Analysis Assumptions and Risks

### 1. Definition of Outliers

Outliers are data points that significantly deviate from the majority of the data. They can be genuine, rare occurrences or errors from measurement, data entry, or other processes. In this project, two primary definitions are used for detection:

* **IQR-based:** A value is an outlier if it falls below `Q1 - 1.5 * IQR` or above `Q3 + 1.5 * IQR`. This method is robust because it's based on quartiles, making it less sensitive to extreme values than the mean and standard deviation.
* **Z-score-based:** A value is an outlier if its absolute Z-score is greater than a specified threshold (e.g., 3.0), meaning it is more than three standard deviations from the mean. This method is effective for data that is approximately normally distributed.

### 2. Handling Methods and Assumptions

We considered two main approaches for handling outliers:

1.  **Filtering (Removing):** Outliers are completely removed from the dataset.
    * **Assumption:** The outliers are considered noise, measurement errors, or anomalies that do not represent the underlying process we are modeling. By removing them, we create a cleaner, more representative dataset for our analysis.

2.  **Winsorizing (Capping):** Outliers are capped at a specific percentile (e.g., the 5th and 95th percentiles).
    * **Assumption:** The extreme values are not errors but are too influential and should be "tamed" rather than discarded entirely. This method preserves all data points, which can be important for time series or small datasets.

### 3. Observed Impact and Risks

Our sensitivity analysis showed that handling outliers has a significant impact on our model. For the linear regression model:

* **Impact:** Removing or winsorizing outliers drastically improves model performance metrics like Mean Absolute Error (MAE) and R². The regression line shifts to better fit the core data, as it is no longer being pulled by extreme points. This indicates that for a simple linear model, outliers are highly influential.
* **Risks:** The greatest risk of this approach is **discarding genuine, meaningful events**. For example, in a financial dataset, a large daily return might be a "black swan" event that contains critical information about market risk. Removing it would cause our model to underestimate future risk, which could be a catastrophic business decision.

Therefore, the choice to remove or winsorize outliers is not just a technical decision but a critical business decision that should be informed by domain knowledge.




## Repo Plan
- **/data/:** Stores tick-level market data CSVs (e.g., price movements for AAP
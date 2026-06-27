# Week 5 Journal

**Name:** Mohit Singh
**Week:** 5
**Topic:** Exploratory Data Analysis (EDA) on Indian Large-Cap Stocks

---

## Day 1 (Monday) – Data Sourcing

### Work Completed

* Built a reusable data loading function using the `yfinance` library.
* Downloaded historical data for five Indian large-cap stocks.
* Organized the data into a consistent format for analysis.

### Challenges Faced

* Initially had some issues understanding the MultiIndex columns returned by `yfinance`.

### Learning

* Learned how to download and organize stock market data efficiently for multiple tickers.

---

## Day 2 (Tuesday) – Data Cleaning

### Work Completed

* Checked dataset dimensions and data types.
* Identified missing values.
* Cleaned the dataset and prepared it for analysis.

### Challenges Faced

* Understood the importance of handling missing values before analysis.

### Learning

* Learned different techniques for inspecting and cleaning financial datasets.

---

## Day 3 (Wednesday) – Feature Engineering

### Work Completed

* Calculated technical indicators:

  * SMA(20)
  * SMA(50)
  * EMA(12)
  * EMA(26)
  * MACD
  * RSI(14)
  * Bollinger Bands
* Visualized price along with technical indicators.

### Challenges Faced

* Faced a few errors while creating Bollinger Bands and plotting them, which were resolved after recalculating the indicator columns.

### Learning

* Understood how technical indicators help identify trends, momentum, and volatility.

---

## Day 4 (Thursday) – Univariate Analysis

### Work Completed

* Visualized distributions of daily returns.
* Analyzed trading volume distribution.
* Examined RSI distribution.
* Created multiple plots for exploratory analysis.

### Challenges Faced

* Encountered plotting errors due to incorrect data formats and resolved them by checking DataFrame columns.

### Learning

* Learned how distributions help identify skewness, spread, and unusual observations.

---

## Day 5 (Friday) – Bivariate Analysis

### Work Completed

* Computed stock return correlations.
* Created a Pearson correlation heatmap.
* Calculated and plotted rolling correlation between Reliance and the Nifty 50.

### Challenges Faced

* Initially forgot to include Nifty data while calculating rolling correlation, resulting in a `NameError`. After downloading the index data separately, the analysis worked correctly.

### Learning

* Learned how rolling correlation changes over time and how it can reveal periods when a stock moves differently from the broader market.

---

## Day 6 (Saturday) – Mini Project

### Work Completed

* Combined all Week 5 tasks into a single EDA report.
* Included:

  * Data summary
  * Missing value analysis
  * Distribution analysis
  * Correlation analysis
  * Feature engineering
  * Rolling correlation
  * Key observations
* Exported the notebook to HTML/PDF for submission.

### Challenges Faced

* Ensured the notebook executed successfully from start to finish without errors and added inline comments to improve readability.

### Learning

* Learned how to structure a complete EDA report that combines data cleaning, visualization, feature engineering, and interpretation into one reproducible notebook.

---

# Overall Reflection

This week strengthened my understanding of Exploratory Data Analysis using real financial data. I became more comfortable with cleaning datasets, engineering technical indicators, creating informative visualizations, and interpreting stock market behavior. I also improved my notebook organization by adding inline comments and maintaining a daily journal, making the work easier to understand and reproduce.

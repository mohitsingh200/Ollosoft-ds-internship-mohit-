# Indian Equities Analytics & Direction Predictor
### Capstone Final Report

**Author:** Mohit Singh 
**Reviewer:** Ravi Agarwal

---

## 1. Problem Statement

Retail and professional investors constantly ask a simple question: *will this
stock go up or down tomorrow?* This capstone frames that question as a
supervised binary classification problem — predict next-day price **direction**
(up vs. down) for 5 Indian large-cap stocks using only historical price/volume
data — and builds a complete, reproducible pipeline around it: data ingestion,
feature engineering, model training/selection, and an interactive dashboard for
exploration.

The goal is not to produce a production trading signal, but to demonstrate a
full, professionally-structured ML workflow end to end, and to honestly report
where such a model succeeds and where it fundamentally struggles.

## 2. Data

**Universe (5 NSE large-caps, chosen for sector diversity and liquidity):**

| Ticker | Company | Sector |
|---|---|---|
| RELIANCE.NS | Reliance Industries | Energy / Conglomerate |
| TCS.NS | Tata Consultancy Services | IT |
| HDFCBANK.NS | HDFC Bank | Banking |
| INFY.NS | Infosys | IT |
| ICICIBANK.NS | ICICI Bank | Banking |

**Source:** Yahoo Finance (`yfinance`), 5 years of daily OHLCV data per ticker.
`src/data.py` caches each ticker to `data/raw/<ticker>.csv` after first fetch.
If `yfinance`/internet is unavailable, the loader deterministically falls back
to a synthetic OHLCV generator so the pipeline remains fully reproducible in
offline environments — clearly logged at runtime, and swappable for real data
with zero code changes once internet access is available.

## 3. Methodology

### 3.1 Exploratory Data Analysis

We examined normalized price performance, daily return distributions and
volatility across the 5 stocks, cross-stock return correlation, and — most
importantly for modeling — the distribution of each engineered feature split
by the next-day-direction target, plus the target's class balance (confirmed
close to 50/50 for every stock, as expected for liquid large-caps).

### 3.2 Feature Engineering

Ten technical-indicator features were engineered per stock from OHLCV data
only (no look-ahead leakage): 1-day return and log-return, price-to-SMA(10)
and price-to-SMA(50) ratios, price-to-EMA(20) ratio, 14-day RSI, MACD
histogram, normalized Bollinger Band width, rolling 10-day return volatility,
and 1-day volume change.

### 3.3 Modeling

Three classifiers were trained and compared:

1. **Logistic Regression** (scaled features, `class_weight='balanced'`) — linear baseline.
2. **Random Forest** (300 trees, depth-limited, balanced classes) — non-linear, robust.
3. **Gradient Boosting** (200 estimators, shallow trees) — non-linear, typically strongest on tabular data.

All models were evaluated with **5-fold `TimeSeriesSplit`** cross-validation —
chronological folds only (no shuffling), so each fold trains strictly on the
past and tests on unseen future data, avoiding look-ahead bias that a
standard random K-fold split would introduce on time series. The
highest-mean-CV-accuracy model was refit on the full dataset and persisted
with `joblib` for use by the dashboard.

### 3.4 Dashboard

An interactive Streamlit app (`app.py`) lets a user pick any of the 5 stocks
and see: a candlestick price chart with SMA/EMA overlays, RSI/MACD/Bollinger
indicator panels, the model's next-day direction prediction with probability,
and a table of historical cross-validated accuracy for all 3 models.

## 4. Results

Cross-validated results (mean over 5 chronological folds, pooled across all 5 stocks):

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.507 | 0.524 | 0.539 | 0.531 |
| Random Forest | 0.501 | 0.517 | 0.531 | 0.523 |
| **Gradient Boosting (selected)** | **0.507** | 0.520 | 0.610 | **0.561** |

*(Exact figures regenerate on every `python run_pipeline.py` run — see `models/metrics.json` for the current values on your data; the table above reflects a representative pipeline run.)*

Gradient Boosting was selected as the best model, primarily on the strength of
its recall/F1, indicating it captures non-linear interactions between
indicators (e.g. RSI extremes combined with MACD histogram sign) slightly
better than the linear baseline. All three models sit close to the 50%
coin-flip line — see Limitations below.

**Figures:** see Appendix for price history, return distribution, rolling
volatility, correlation matrix, feature distributions by class, model
comparison chart, per-fold accuracy stability, and feature importances.

## 5. Limitations

- **Accuracy near the random-walk baseline.** This is the single most
  important finding: short-horizon (1-day) direction prediction on liquid,
  well-covered large-cap stocks is close to weak-form market-efficient,
  meaning historical price/volume patterns alone carry very limited signal
  for tomorrow's direction. This matches published academic findings, not a
  pipeline defect.
- **No fundamental, macro, or sentiment data.** Only technical indicators
  derived from price/volume were used.
- **Binary framing loses information.** Treating this as a hard up/down call
  discards the magnitude of the move and the model's confidence (though the
  dashboard does expose predicted probability).
- **Per-stock, not portfolio-level.** No cross-stock, sector, or
  market-relative features were used.
- **No transaction-cost-aware backtest.** Accuracy alone does not translate
  into profitability; a proper backtest with costs, slippage and position
  sizing is required before any real-world use.

## 6. Future Work

- Add fundamental data (EPS, P/E), macro variables (Nifty 50, USD/INR, crude
  oil for RELIANCE), and news/sentiment features.
- Predict a probability/confidence score and size a signal accordingly,
  rather than a hard binary label.
- Extend to multi-day or weekly horizons, where technical signals may carry
  more information than at 1-day horizon.
- Add a proper walk-forward backtest with transaction costs and realistic
  position sizing to evaluate economic (not just statistical) value.
- Explore sequence models (LSTM/Transformer) on raw price sequences as a
  comparison point to the current tabular-feature approach.
- Add a rolling retraining schedule (e.g. monthly) to simulate a production
  deployment.

## 7. Conclusion

This capstone delivers a fully reproducible, single-command pipeline covering
data ingestion, feature engineering, model comparison with sound
time-series cross-validation, and an interactive dashboard. The headline
result — that next-day direction on large-cap Indian equities is only
marginally more predictable than a coin flip using technical indicators alone
— is itself a meaningful, honestly-reported finding, and the codebase is
structured to make extending toward more predictive feature sets
straightforward.

---

## Appendix — Figures

*(See `reports/fig_*.png` for source images; `final_report.pdf` embeds all 8 figures generated by this exact pipeline run.)*

1. Normalized price performance, all 5 stocks
2. Daily return distribution by stock
3. Rolling 30-day annualized volatility
4. Return correlation matrix
5. Feature distributions split by next-day direction
6. Model comparison (accuracy / precision / recall / F1)
7. Per-fold accuracy stability across time
8. Feature importances (best model)

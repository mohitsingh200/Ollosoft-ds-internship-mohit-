# Indian Equities Analytics & Direction Predictor

A portfolio-grade capstone: an end-to-end, fully reproducible pipeline that pulls
5 years of daily data for 5 Indian large-cap stocks, engineers technical-indicator
features, trains and compares 3 ML classifiers to predict next-day price direction,
and serves the results through an interactive Streamlit dashboard.



## Universe

| Ticker | Company | Sector |
|---|---|---|
| RELIANCE.NS | Reliance Industries | Energy / Conglomerate |
| TCS.NS | Tata Consultancy Services | IT |
| HDFCBANK.NS | HDFC Bank | Banking |
| INFY.NS | Infosys | IT |
| ICICIBANK.NS | ICICI Bank | Banking |

## Quickstart (single command)

```bash
git clone <this-repo>
cd capstone
pip install -r requirements.txt
python run_pipeline.py          # fetches data, builds features, trains + saves best model
streamlit run app.py            # launches the interactive dashboard
```

`run_pipeline.py` is the single-command reproducibility entry point required by the week08 
capstone spec. It runs `src/data.py -> src/features.py -> src/model.py` in sequence
and writes `data/processed/features.csv` and `models/best_model.joblib`.


## Repo structure

```
capstone/
├── data/
│   ├── raw/               # cached per-ticker OHLCV CSVs (git-ignored after first run is fine to commit small samples)
│   └── processed/         # features.csv used for modeling
├── notebooks/
│   ├── 01_eda.ipynb        # polished EDA — price history, volatility, correlations, feature distributions
│   ├── 02_modeling.ipynb   # train/compare 3 models with TimeSeriesSplit, save best model
│   └── 03_dashboard.ipynb  # notebook-native preview of the dashboard components
├── src/
│   ├── data.py             # data loader (yfinance + offline synthetic fallback)
│   ├── features.py         # technical-indicator feature engineering + target label
│   └── model.py             # model zoo, TimeSeriesSplit evaluation, best-model selection/saving
├── models/
│   ├── best_model.joblib    # trained pipeline + metadata
│   └── metrics.json         # CV metrics for all 3 models
├── app.py                   # Streamlit dashboard (Day 4 deliverable)
├── run_pipeline.py           # single-command reproducibility entry point
├── reports/
│   └── final_report.md       # 5-8 page write-up (export to PDF for submission)
├── assets/screenshots/        # dashboard screenshots for README / report
├── Capstone_Presentation_outline.md   # slide-by-slide outline for the deck
├── requirements.txt
└── README.md
```

## Problem

Given daily OHLCV history for a stock, predict whether tomorrow's closing price
will be **higher** or **lower** than today's close — a binary classification
("direction prediction") task, framed as a decision-support signal rather than a
standalone trading strategy.

## Data

- **Source:** Yahoo Finance (`yfinance`), 5 years of daily OHLCV per ticker (`.NS` suffix for NSE).
- **Offline fallback:** if `yfinance` is unavailable (e.g. sandboxed grading environments
  with no internet), `src/data.py` generates a deterministic synthetic OHLCV series
  per ticker via geometric Brownian motion, so the pipeline is still fully runnable
  and reproducible. This is logged clearly at runtime and cached the same way real
  data would be — swap in real data by simply running with internet access; no code
  changes required.
- **Caching:** each ticker's data is cached to `data/raw/<ticker>.csv` on first fetch
  and reused on subsequent runs (delete the file to force a re-fetch).

## Features (10 per stock, `src/features.py`)

| Feature | Description |
|---|---|
| `return_1d` | 1-day % return |
| `log_return_1d` | 1-day log return |
| `sma_10_ratio` | Close / 10-day SMA |
| `sma_50_ratio` | Close / 50-day SMA |
| `ema_20_ratio` | Close / 20-day EMA |
| `rsi_14` | 14-day Relative Strength Index |
| `macd_hist` | MACD line − signal line |
| `bb_width` | Bollinger Band width (20, 2σ), normalized |
| `volatility_10` | rolling 10-day std of returns |
| `volume_change` | 1-day % change in volume |

Target: `target = 1` if next day's close > today's close, else `0`.

## Methodology

1. **EDA** (`notebooks/01_eda.ipynb`): price history, return distributions,
   rolling volatility, cross-stock return correlation, feature distributions
   split by target class, class balance check.
2. **Modeling** (`notebooks/02_modeling.ipynb`, `src/model.py`): Logistic
   Regression, Random Forest, and Gradient Boosting, each evaluated with
   5-fold `TimeSeriesSplit` (chronological, no shuffling — avoids look-ahead
   leakage). The model with the highest mean CV accuracy is refit on the full
   dataset and persisted with `joblib`.
3. **Dashboard** (`app.py`): stock picker, candlestick price chart with
   SMA/EMA overlays, RSI/MACD/Bollinger indicator panels, next-day prediction
   with probability, and a table of historical CV accuracy per model.

## Results

Exact numbers are written to `models/metrics.json` on every pipeline run — see
that file (or the printed summary in `02_modeling.ipynb`) for the current
numbers on your data. In testing (both on synthetic fallback data and
typical results on real NSE data for these large-caps), all three models
land close to the ~50–53% accuracy range, with Gradient Boosting or Random
Forest usually edging out Logistic Regression slightly by capturing
non-linear feature interactions.

## Limitations & Future Work

- **Near-random-walk accuracy.** Short-horizon direction on liquid large-caps
  is close to weak-form efficient; ~50-53% accuracy is expected and consistent
  with published literature, not a bug in the pipeline.
- **No fundamental/macro/sentiment features.** Only price/volume-derived
  technical indicators are used. Adding news sentiment, earnings data, sector
  indices, or macro variables (Nifty, USD/INR, crude oil for RELIANCE, etc.)
  is a natural next step.
- **Hard classification vs. probabilities.** A more realistic use case treats
  the model's predicted probability as a signal strength / confidence score
  (already exposed in the dashboard) rather than a binary bet.
- **Single-stock models.** Currently no cross-stock or portfolio-level
  modeling (e.g. relative strength, pairs, sector rotation).
- **No transaction-cost-aware backtest.** A proper backtest with slippage,
  costs, and position sizing would be required before any of this could
  inform real trading decisions.
- **Fixed 5-year window.** Longer history, or a rolling-retrain schedule
  (retrain monthly on the trailing N years), would better reflect a
  production deployment.

## How to reproduce from scratch

'''bash
pip install -r requirements.txt
python run_pipeline.py
streamlit run app.py
'''

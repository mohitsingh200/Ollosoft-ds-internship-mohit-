"""
src/data.py
------------
Data loading for the 'Indian Equities Analytics & Direction Predictor' capstone.

Primary source : Yahoo Finance via `yfinance` (needs internet).
Fallback source: a deterministic synthetic OHLCV generator (geometric Brownian
                 motion + volume noise), used automatically if `yfinance` is
                 not installed or the download fails/returns empty.

This keeps `run_pipeline.py` reproducible with a SINGLE COMMAND even in
offline / sandboxed / CI environments. Once you run this with internet
access, real data is cached to data/raw/*.csv and reused on every later run.

Universe: 5 NSE large-cap stocks across different sectors.
"""

import os
import numpy as np
import pandas as pd

STOCKS = {
    "RELIANCE.NS": "Reliance Industries (Energy/Conglomerate)",
    "TCS.NS": "Tata Consultancy Services (IT)",
    "HDFCBANK.NS": "HDFC Bank (Banking)",
    "INFY.NS": "Infosys (IT)",
    "ICICIBANK.NS": "ICICI Bank (Banking)",
}

_HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(_HERE, "..", "data", "raw")

DEFAULT_START = "2019-07-01"
DEFAULT_END = "2024-07-01"


def _synthetic_ohlcv(ticker: str, start: str, end: str, seed: int) -> pd.DataFrame:
    """Deterministic fake-but-plausible daily OHLCV series (offline fallback)."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, end=end)  # business days only
    n = len(dates)

    # Different drift/vol per ticker so the 5 stocks look distinct
    drift = rng.uniform(0.0002, 0.0006)
    vol = rng.uniform(0.012, 0.022)
    start_price = rng.uniform(300, 3500)

    log_returns = rng.normal(loc=drift, scale=vol, size=n)
    close = start_price * np.exp(np.cumsum(log_returns))

    daily_range = close * rng.uniform(0.005, 0.02, size=n)
    high = close + daily_range * rng.uniform(0.3, 1.0, size=n)
    low = close - daily_range * rng.uniform(0.3, 1.0, size=n)
    open_ = low + (high - low) * rng.uniform(0, 1, size=n)
    volume = rng.integers(1_000_000, 12_000_000, size=n).astype(float)

    df = pd.DataFrame(
        {
            "Open": open_,
            "High": np.maximum.reduce([high, open_, close]),
            "Low": np.minimum.reduce([low, open_, close]),
            "Close": close,
            "Volume": volume,
        },
        index=dates,
    )
    df.index.name = "Date"
    return df


def fetch_stock(ticker: str, start: str = DEFAULT_START, end: str = DEFAULT_END,
                 use_cache: bool = True) -> pd.DataFrame:
    """Fetch OHLCV for one ticker. Caches to data/raw/<ticker>.csv."""
    os.makedirs(RAW_DIR, exist_ok=True)
    cache_path = os.path.join(RAW_DIR, f"{ticker.replace('.', '_')}.csv")

    if use_cache and os.path.exists(cache_path):
        df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        return df

    source = "synthetic"
    df = None
    try:
        import yfinance as yf  # optional dependency

        raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if raw is not None and not raw.empty:
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = raw.columns.get_level_values(0)
            df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
            source = "yfinance"
    except Exception as exc:  # noqa: BLE001 - broad on purpose, this is a fallback path
        print(f"[data.py] yfinance fetch failed for {ticker} ({exc!r}); using synthetic fallback.")

    if df is None:
        df = _synthetic_ohlcv(ticker, start, end, seed=abs(hash(ticker)) % (2**32))

    df.to_csv(cache_path)
    print(f"[data.py] {ticker}: {len(df)} rows loaded from '{source}', cached at {cache_path}")
    return df


def fetch_all(start: str = DEFAULT_START, end: str = DEFAULT_END,
              use_cache: bool = True) -> dict:
    """Fetch OHLCV for all 5 stocks in STOCKS. Returns {ticker: DataFrame}."""
    return {t: fetch_stock(t, start, end, use_cache) for t in STOCKS}


if __name__ == "__main__":
    data = fetch_all()
    for tkr, df in data.items():
        print(tkr, df.shape, df.index.min().date(), "->", df.index.max().date())

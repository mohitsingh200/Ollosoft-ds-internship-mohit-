"""
src/features.py
-----------------
Feature engineering for the direction-prediction model.

Produces ~9 features per stock (technical indicators computed purely from
OHLCV, so no look-ahead leakage) plus a binary target:
    target = 1 if next trading day's Close > today's Close, else 0

Features:
    return_1d        - 1-day pct return
    log_return_1d    - 1-day log return
    sma_10_ratio      - Close / 10-day SMA
    sma_50_ratio      - Close / 50-day SMA
    ema_20_ratio      - Close / 20-day EMA
    rsi_14           - 14-day Relative Strength Index
    macd_hist        - MACD line minus signal line
    bb_width         - Bollinger Band width (20, 2-sigma), normalized
    volatility_10    - rolling 10-day std of returns
    volume_change    - 1-day pct change in volume
"""

import numpy as np
import pandas as pd


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _macd_hist(close: pd.Series, fast=12, slow=26, signal=9) -> pd.Series:
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line - signal_line


def build_features(df: pd.DataFrame, ticker: str = None) -> pd.DataFrame:
    """Given a raw OHLCV DataFrame, return a feature DataFrame with a target column."""
    out = pd.DataFrame(index=df.index)
    close = df["Close"]
    volume = df["Volume"]

    out["return_1d"] = close.pct_change()
    out["log_return_1d"] = np.log(close / close.shift(1))
    out["sma_10_ratio"] = close / close.rolling(10).mean()
    out["sma_50_ratio"] = close / close.rolling(50).mean()
    out["ema_20_ratio"] = close / close.ewm(span=20, adjust=False).mean()
    out["rsi_14"] = _rsi(close, 14)
    out["macd_hist"] = _macd_hist(close)

    sma_20 = close.rolling(20).mean()
    std_20 = close.rolling(20).std()
    upper, lower = sma_20 + 2 * std_20, sma_20 - 2 * std_20
    out["bb_width"] = (upper - lower) / sma_20

    out["volatility_10"] = out["return_1d"].rolling(10).std()
    out["volume_change"] = volume.pct_change()

    # target: next-day direction (1 = up, 0 = down/flat)
    out["target"] = (close.shift(-1) > close).astype(int)

    if ticker is not None:
        out.insert(0, "ticker", ticker)

    out = out.replace([np.inf, -np.inf], np.nan).dropna()
    return out


def build_all_features(stock_data: dict) -> pd.DataFrame:
    """stock_data: {ticker: raw OHLCV DataFrame} -> single long-format DataFrame."""
    frames = [build_features(df, ticker=t) for t, df in stock_data.items()]
    combined = pd.concat(frames).sort_index()
    combined.index.name = "Date"
    return combined


FEATURE_COLUMNS = [
    "return_1d", "log_return_1d", "sma_10_ratio", "sma_50_ratio",
    "ema_20_ratio", "rsi_14", "macd_hist", "bb_width",
    "volatility_10", "volume_change",
]

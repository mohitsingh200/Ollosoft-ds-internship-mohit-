"""
app.py
-------
Streamlit dashboard for the 'Indian Equities Analytics & Direction Predictor' capstone.

Run:
    streamlit run app.py

Lets the user:
    - pick one of the 5 stocks
    - see the price chart with SMA/EMA overlays
    - see technical indicators (RSI, MACD histogram, Bollinger width)
    - see tomorrow's predicted direction from the saved best model
    - see the model's historical (walk-forward) accuracy over time

Assumes `python run_pipeline.py` has already been run at least once so that
data/processed/features.csv and models/best_model.joblib exist.
"""

import os

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from src.data import STOCKS, fetch_stock
from src.features import FEATURE_COLUMNS, build_features
from src.model import evaluate_with_tscv, MODEL_ZOO

st.set_page_config(page_title="Indian Equities Direction Predictor", layout="wide")

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(HERE, "models", "best_model.joblib")
METRICS_PATH = os.path.join(HERE, "models", "metrics.json")


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


@st.cache_data(ttl=3600)
def load_stock(ticker):
    raw = fetch_stock(ticker)
    feats = build_features(raw, ticker=ticker)
    return raw, feats


st.title("📈 Indian Equities Analytics & Direction Predictor")
st.caption(
    "Educational capstone project — NOT investment advice. "
    "Predictions are next-day UP/DOWN direction probabilities from a model "
    "trained on historical technical indicators."
)

ticker = st.sidebar.selectbox(
    "Choose a stock",
    options=list(STOCKS.keys()),
    format_func=lambda t: f"{t} — {STOCKS[t]}",
)
lookback_days = st.sidebar.slider("Chart lookback (trading days)", 60, 750, 250)

raw, feats = load_stock(ticker)
bundle = load_model()

if raw.attrs.get("source") == "synthetic":
    st.sidebar.warning(
        "Running on synthetic offline data (yfinance unavailable in this "
        "environment). Run locally with internet access for real NSE data — "
        "the pipeline and model logic are identical either way."
    )

col_price, col_pred = st.columns([3, 1])

# ---- Price chart with SMA/EMA overlays -----------------------------------
with col_price:
    st.subheader(f"{ticker} — Price & Moving Averages")
    plot_df = raw.tail(lookback_days).copy()
    plot_df["SMA_10"] = raw["Close"].rolling(10).mean().tail(lookback_days)
    plot_df["SMA_50"] = raw["Close"].rolling(50).mean().tail(lookback_days)
    plot_df["EMA_20"] = raw["Close"].ewm(span=20, adjust=False).mean().tail(lookback_days)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=plot_df.index, open=plot_df["Open"], high=plot_df["High"],
        low=plot_df["Low"], close=plot_df["Close"], name="Price",
    ))
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df["SMA_10"], name="SMA 10", line=dict(width=1)))
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df["SMA_50"], name="SMA 50", line=dict(width=1)))
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df["EMA_20"], name="EMA 20", line=dict(width=1, dash="dot")))
    fig.update_layout(height=450, xaxis_rangeslider_visible=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ---- Next-day prediction card ---------------------------------------------
with col_pred:
    st.subheader("Next-Day Prediction")
    if bundle is None:
        st.error("No trained model found. Run `python run_pipeline.py` first.")
    else:
        model, model_name = bundle["model"], bundle["name"]
        latest_row = feats.iloc[[-1]][FEATURE_COLUMNS]
        proba_up = model.predict_proba(latest_row)[0][1]
        direction = "UP ▲" if proba_up >= 0.5 else "DOWN ▼"
        st.metric("Predicted direction", direction, f"{proba_up:.0%} prob. of UP")
        st.caption(f"Model: **{model_name}**")
        st.progress(min(max(proba_up, 0.0), 1.0))

# ---- Technical indicators ---------------------------------------------
st.subheader("Technical Indicators")
ind_df = feats.tail(lookback_days)
ind_fig = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.34, 0.33, 0.33],
                         subplot_titles=("RSI (14)", "MACD Histogram", "Bollinger Band Width"))
ind_fig.add_trace(go.Scatter(x=ind_df.index, y=ind_df["rsi_14"], name="RSI 14"), row=1, col=1)
ind_fig.add_hline(y=70, line_dash="dot", line_color="red", row=1, col=1)
ind_fig.add_hline(y=30, line_dash="dot", line_color="green", row=1, col=1)
ind_fig.add_trace(go.Bar(x=ind_df.index, y=ind_df["macd_hist"], name="MACD hist"), row=2, col=1)
ind_fig.add_trace(go.Scatter(x=ind_df.index, y=ind_df["bb_width"], name="BB width"), row=3, col=1)
ind_fig.update_layout(height=550, showlegend=False, margin=dict(t=40, b=20))
st.plotly_chart(ind_fig, use_container_width=True)

# ---- Historical model accuracy -----------------------------------------
st.subheader("Historical Model Accuracy (TimeSeriesSplit, all 5 stocks)")
if os.path.exists(METRICS_PATH):
    import json
    with open(METRICS_PATH) as f:
        metrics = json.load(f)
    metrics_df = pd.DataFrame(metrics["results"]).T
    st.dataframe(metrics_df.style.format("{:.3f}").highlight_max(axis=0, color="lightgreen"))
    st.caption(
        f"Best model selected: **{metrics['best_model']}**. "
        "Accuracy near 50% reflects the well-known difficulty of predicting "
        "short-horizon direction for liquid large-cap equities — see README "
        "Limitations for discussion."
    )
else:
    st.info("Run `python run_pipeline.py` to generate model metrics.")

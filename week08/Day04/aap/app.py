import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib

# ----------------------------
# Load data
# ----------------------------

data = pd.read_csv("../data/features.csv")

model = joblib.load("../models/best_model.joblib")

# ----------------------------
# Feature columns
# ----------------------------

feature_columns = [
    "SMA_10",
    "SMA_20",
    "SMA_50",
    "EMA_10",
    "EMA_20",
    "RSI",
    "MACD",
    "Lag_1",
    "Lag_5",
    "Lag_21"
]

# ----------------------------
# Dashboard title
# ----------------------------

st.title("Indian Equities Analytics Dashboard")

# ----------------------------
# If Ticker column exists
# ----------------------------

if "Ticker" in data.columns:

    stocks = sorted(data["Ticker"].unique())

    stock = st.selectbox("Select Stock", stocks)

    df = data[data["Ticker"] == stock].copy()

else:

    st.warning("Ticker column not found.")

    stock = "Current Dataset"

    df = data.copy()

# ----------------------------
# Price Chart
# ----------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Close"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SMA_20"],
        name="SMA20"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA_20"],
        name="EMA20"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# RSI
# ----------------------------

st.subheader("RSI")

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI"
    )
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# MACD
# ----------------------------

st.subheader("MACD")

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MACD"],
        name="MACD"
    )
)

fig3.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Signal"],
        name="Signal"
    )
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Prediction
# ----------------------------

st.subheader("Next Day Prediction")

latest = df.iloc[-1]

X_latest = latest[feature_columns].values.reshape(1, -1)

prediction = model.predict(X_latest)[0]

if prediction == 1:
    st.success("Prediction : UP")
else:
    st.error("Prediction : DOWN")

# ----------------------------
# Historical Accuracy
# ----------------------------

if "Prediction" in df.columns:

    accuracy = (df["Prediction"] == df["Target"]).mean() * 100

    st.metric("Historical Accuracy", f"{accuracy:.2f}%")
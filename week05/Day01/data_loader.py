import pandas as pd
import yfinance as yf


def fetch_stocks(tickers, start, end):

# Download historical data from Yahoo Finance
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True
    )

    close = data["Close"]
# Convert wide format into tidy long format
    long_df = (
        close
        .reset_index()
        .melt(
            id_vars="Date",
            var_name="Ticker",
            value_name="Close"
        )
    )

    return long_df 
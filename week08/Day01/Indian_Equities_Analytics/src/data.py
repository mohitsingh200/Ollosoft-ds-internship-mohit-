"""
Reusable Data Loader
"""

import yfinance as yf


def download_stock_data(
    tickers,
    start,
    end
):
    """
    Download stock data
    """

    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        group_by="ticker"
    )

    return data


def save_data(
    dataframe,
    path
):
    """
    Save dataframe as CSV
    """

    dataframe.to_csv(path)

    print("Dataset saved successfully.")
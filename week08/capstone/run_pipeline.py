#!/usr/bin/env python3
"""
run_pipeline.py
-----------------
Single-command entry point for the whole capstone:

    python run_pipeline.py

Steps:
    1. Fetch 5 years of OHLCV data for 5 NSE large-caps (src/data.py)
    2. Engineer technical-indicator features + next-day-direction target (src/features.py)
    3. Train Logistic Regression / Random Forest / Gradient Boosting with
       TimeSeriesSplit CV, save the best model (src/model.py)
    4. Print a summary report to the console

After this runs, `data/processed/features.csv` and `models/best_model.joblib`
exist and notebooks/app.py can use them directly.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data import fetch_all, STOCKS  # noqa: E402
from src.features import build_all_features  # noqa: E402
from src.model import train_and_select_best  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PROCESSED_PATH = os.path.join(HERE, "data", "processed", "features.csv")


def main():
    t0 = time.time()
    print("=" * 60)
    print("Indian Equities Analytics & Direction Predictor")
    print(f"Universe: {list(STOCKS.keys())}")
    print("=" * 60)

    print("\n[1/3] Fetching data...")
    stock_data = fetch_all()

    print("\n[2/3] Engineering features...")
    features_df = build_all_features(stock_data)
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    features_df.to_csv(PROCESSED_PATH)
    print(f"  -> {features_df.shape[0]} rows x {features_df.shape[1]} cols saved to {PROCESSED_PATH}")

    print("\n[3/3] Training models...")
    result = train_and_select_best(features_df)

    print("\n" + "=" * 60)
    print(f"DONE in {time.time() - t0:.1f}s")
    print(f"Best model : {result['best_model']}")
    print(f"Model file : {result['model_path']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
src/model.py
-------------
Train and evaluate 3 classifiers to predict next-day stock direction:
    - Logistic Regression
    - Random Forest
    - Gradient Boosting

Uses sklearn TimeSeriesSplit (no shuffling / no look-ahead across folds).
Saves the best model (by mean CV accuracy) to models/best_model.joblib,
along with a metrics summary to models/metrics.json.
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURE_COLUMNS

_HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(_HERE, "..", "models")

MODEL_ZOO = {
    "logistic_regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ]),
    "random_forest": Pipeline([
        ("clf", RandomForestClassifier(
            n_estimators=300, max_depth=6, min_samples_leaf=20,
            class_weight="balanced", random_state=42, n_jobs=-1,
        )),
    ]),
    "gradient_boosting": Pipeline([
        ("clf", GradientBoostingClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42,
        )),
    ]),
}


def evaluate_with_tscv(model, X: pd.DataFrame, y: pd.Series, n_splits: int = 5) -> dict:
    tscv = TimeSeriesSplit(n_splits=n_splits)
    fold_metrics = []
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        fold_metrics.append({
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1": f1_score(y_test, preds, zero_division=0),
        })
    avg = {k: float(np.mean([m[k] for m in fold_metrics])) for k in fold_metrics[0]}
    avg["fold_metrics"] = fold_metrics
    return avg


def train_and_select_best(features_df: pd.DataFrame) -> dict:
    """
    features_df must contain FEATURE_COLUMNS + 'target', sorted by Date.
    Returns a results dict and writes best_model.joblib + metrics.json to models/.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    X = features_df[FEATURE_COLUMNS]
    y = features_df["target"]

    results = {}
    for name, pipeline in MODEL_ZOO.items():
        print(f"[model.py] Evaluating {name} with TimeSeriesSplit...")
        metrics = evaluate_with_tscv(pipeline, X, y)
        results[name] = metrics
        print(f"  -> acc={metrics['accuracy']:.3f} f1={metrics['f1']:.3f}")

    best_name = max(results, key=lambda n: results[n]["accuracy"])
    print(f"[model.py] Best model: {best_name} (acc={results[best_name]['accuracy']:.3f})")

    # Refit best model on ALL data for deployment / dashboard use
    best_pipeline = MODEL_ZOO[best_name]
    best_pipeline.fit(X, y)

    model_path = os.path.join(MODELS_DIR, "best_model.joblib")
    joblib.dump({"model": best_pipeline, "name": best_name, "features": FEATURE_COLUMNS}, model_path)

    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    clean_results = {
        n: {k: v for k, v in m.items() if k != "fold_metrics"} for n, m in results.items()
    }
    with open(metrics_path, "w") as f:
        json.dump({"best_model": best_name, "results": clean_results}, f, indent=2)

    print(f"[model.py] Saved best model -> {model_path}")
    print(f"[model.py] Saved metrics    -> {metrics_path}")

    return {"best_model": best_name, "results": results, "model_path": model_path}


if __name__ == "__main__":
    processed_path = os.path.join(_HERE, "..", "data", "processed", "features.csv")
    df = pd.read_csv(processed_path, index_col=0, parse_dates=True)
    train_and_select_best(df)

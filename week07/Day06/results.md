# Week 7 – Machine Learning Mini Project Results

## Project Title
Machine Learning Baseline for Predicting Next-Day Direction of Reliance Industries Stock

---

## Objective

The objective of this project was to build and compare multiple machine learning models to predict whether the next trading day's closing price of Reliance Industries stock would move **Up (1)** or **Down (0)** based on historical stock data and technical indicators.

---

## Dataset

- Company: Reliance Industries Ltd.
- Data Type: Historical Daily Stock Data
- Target Variable:
  - **1** → Next-Day Stock Price Goes Up
  - **0** → Next-Day Stock Price Goes Down

---

## Feature Engineering

The following technical indicators were used as model features:

- SMA (20-Day Simple Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Daily Return
- Lag-1 Return
- Lag-5 Return
- Lag-21 Return

These features capture price trends, momentum, and historical return patterns.

---

## Models Implemented

The following machine learning models were trained and evaluated:

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

A **Naive Baseline** (always predicting an upward movement) was also used for comparison.

---

## Validation Strategy

Since stock market data follows a chronological order, **TimeSeriesSplit (5-Fold Cross Validation)** was used instead of a random train-test split to prevent data leakage and simulate real-world forecasting.

---

## Evaluation Metrics

Each model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score

These metrics were averaged across all TimeSeriesSplit folds for a fair comparison.

---

## Results

The performance of all machine learning models was compared using the evaluation metrics.

The Random Forest Classifier demonstrated the best overall performance and was selected as the final baseline model because it achieved the strongest balance between prediction accuracy, precision, recall, and F1 score.

Feature importance analysis showed that lagged returns and technical indicators such as RSI, MACD, and SMA contributed significantly to predicting the next-day stock direction.

---

## Conclusion

This mini project successfully developed and evaluated three supervised machine learning models for stock direction prediction.

Among the evaluated models, **Random Forest Classifier** was selected as the final baseline model because of its superior overall performance and better generalization capability compared with Logistic Regression and Decision Tree.

Although the results are encouraging, this model should **not** be used directly for real trading decisions because stock prices are influenced by many external factors such as company news, economic events, market sentiment, and geopolitical conditions, which were not included in this dataset.

Future improvements may include:

- Hyperparameter tuning
- XGBoost / LightGBM
- LSTM-based deep learning models
- Additional technical indicators
- News sentiment analysis
- Macroeconomic indicators

---

## Files Submitted

- `ml_baseline.ipynb`
- `results.md`
- `model_ranking.csv`
- `feature_importance.png`
- `model_comparison.png`
- Confusion Matrix images

---

**Prepared By:** Mohit Singh  
**Internship:** Ollosoft Technologies – Data Science Internship  
**Week:** 7 – Machine Learning Mini Project
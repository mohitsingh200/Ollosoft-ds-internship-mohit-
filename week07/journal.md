# Week 7 Journal
**Name:** Mohit Singh

**Week:** 7

**Topic:** Machine Learning Baseline for Stock Direction Prediction

---

## Objective

The objective of this week's assignment was to learn the fundamentals of supervised machine learning for financial data. The work focused on predicting the next-day stock price direction using technical indicators and evaluating multiple machine learning models.

---

## Day 1 – Feature Engineering

### Tasks Completed

- Prepared the machine learning dataset.
- Created feature matrix (X).
- Created target variable (next-day movement).
- Used TimeSeriesSplit for time-series-aware data splitting.

### Features Used

- SMA(20)
- RSI
- MACD
- Lag_1
- Lag_5
- Lag_21

---

## Day 2 – Linear Regression

### Tasks Completed

- Trained a Linear Regression model.
- Predicted next-day returns.
- Evaluated using:
  - RMSE
  - MAE
- Plotted Actual vs Predicted Returns.

### Observation

Linear Regression captured the overall trend but struggled to predict daily market fluctuations accurately.

---

## Day 3 – Logistic Regression

### Tasks Completed

- Converted the target into a binary classification problem.
- Built a Logistic Regression classifier.
- Evaluated using:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
- Generated a confusion matrix.

### Observation

The Logistic Regression model served as a simple baseline and produced stable classification performance.

---

## Day 4 – Decision Tree and Random Forest

### Tasks Completed

- Trained a Decision Tree Classifier.
- Trained a Random Forest Classifier.
- Compared model performance.
- Generated feature importance plots.

### Observation

Random Forest achieved better generalization and more stable predictions than the Decision Tree.

---

## Day 5 – Model Evaluation

### Tasks Completed

- Applied 5-fold TimeSeriesSplit cross-validation.
- Compared:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Naive Baseline (Always Predict Up)
- Calculated:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
- Ranked all models.

### Observation

Random Forest achieved the highest overall performance based on the F1 Score and showed the best balance between precision and recall.

---

## Challenges Faced

- Continuous target values caused classification errors.
- Missing values in engineered features.
- Incorrect target labels.
- TimeSeriesSplit issues due to class imbalance.
- CSV formatting and missing Date column.

---

## Skills Learned

- Feature engineering
- Time-series cross-validation
- Binary classification
- Logistic Regression
- Decision Tree
- Random Forest
- Model evaluation
- Feature importance analysis
- Confusion matrix interpretation

---

## Key Takeaways

Machine learning models can identify useful patterns from engineered technical indicators. Among the tested models, Random Forest provided the best overall predictive performance and outperformed the naive baseline.

---

## Next Week Goals

- Learn advanced ensemble methods.
- Explore Gradient Boosting and XGBoost.
- Improve feature engineering techniques.
- Optimize model performance through hyperparameter tuning.
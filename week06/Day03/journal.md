## Day 3 (Wednesday) – Time Series Decomposition

### Work Completed
- Studied the concept of time series decomposition.
- Resampled Reliance daily closing prices to monthly frequency.
- Applied the `seasonal_decompose()` function from `statsmodels`.
- Visualized the observed, trend, seasonal, and residual components.
- Interpreted the contribution of each component to the overall time series.

### Challenges Faced
- Learned the importance of selecting an appropriate seasonal period (`period=12`) for monthly data.
- Compared additive decomposition with the structure of financial time series.

### Learning
- Understood how decomposition separates a time series into trend, seasonal, and residual components.
- Learned that stock prices often exhibit a clear trend but relatively weak seasonal behavior.
- Recognized decomposition as a valuable exploratory step before building forecasting models. 
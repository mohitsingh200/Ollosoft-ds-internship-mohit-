#Day 1 (Monday) – Time Series Fundamentals
##Work Completed
1. Downloaded historical Reliance Industries stock data using the yfinance library.
2. Verified that the dataset uses a DatetimeIndex, which is essential for time series analysis.
3. Resampled daily stock data into weekly and monthly frequencies.
4. Created lag features:
    -Lag-1 (previous trading day)
    -Lag-5 (previous trading week)
    -Lag-21 (previous trading month)
5. Saved the processed dataset for future forecasting tasks.
##Challenges Faced
   Initially reviewed how the resample() method works and understood the difference between weekly and monthly aggregation.
##Learning
    -Learned the importance of DatetimeIndex in time series analysis.
    -Understood how resampling changes the frequency of observations.
    -Learned how lag features capture past information and are commonly used in forecasting models.
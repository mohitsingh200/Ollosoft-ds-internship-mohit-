# Week 6 – Day 6 Journal


## Objective

The objective of today's task was to forecast the Nifty 50 monthly closing price for the next six months using an ARIMA(1,1,1) model and visualize the forecast with confidence intervals.

---

## Tasks Completed

- Loaded the cleaned Nifty 50 dataset.
- Converted the Date column to DatetimeIndex.
- Resampled daily data into monthly closing prices.
- Built an ARIMA(1,1,1) forecasting model.
- Generated a six-month forecast.
- Plotted historical prices and forecasted prices.
- Added 95% confidence intervals to the forecast plot.
- Saved the forecast figure.
- Interpreted the forecasting results.

---

## Challenges Faced

- Encountered a **FileNotFoundError** because the dataset path was incorrect.
- Corrected the file location and updated the CSV path.
- Verified the working directory before loading the dataset.
- Successfully generated the forecast after fixing the path.

---

## Key Learnings

- Learned how ARIMA models are used for time series forecasting.
- Understood the importance of monthly resampling before forecasting.
- Learned how to generate future forecasts using the `get_forecast()` method.
- Learned how to visualize confidence intervals along with predicted values.
- Understood that ARIMA models rely only on historical data and have limitations for real-world stock prediction.

---

## Files Created

- `mini_task.ipynb`
- `forecast.png`
- `journal.md`


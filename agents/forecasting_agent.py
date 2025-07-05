### --- /agents/forecasting_agent.py ---
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def forecast_prices(prices):
    model = ARIMA(prices, order=(2,1,2))
    fit = model.fit()
    forecast = fit.forecast(steps=1)[0]
    trend = "upward" if forecast > prices[-1] else "downward"

    return {
        "predicted_price": round(forecast, 2),
        "trend": trend
    }

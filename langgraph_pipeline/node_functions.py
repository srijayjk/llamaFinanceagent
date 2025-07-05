from agents.forecasting_agent import forecast_prices
from agents.sentiment_agent import fetch_sentiment_data
from agents.langchain_agent import respond_to_forecast

def forecast_node(state):
    state["forecast"] = forecast_prices(state["prices"])
    return state

def sentiment_node(state):
    state["sentiment"] = fetch_sentiment_data(state["symbol"])
    return state

def llm_node(state):
    state["explanation"] = respond_to_forecast(state)
    return state
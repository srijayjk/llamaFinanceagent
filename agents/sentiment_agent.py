### --- /agents/sentiment_agent.py ---
import finnhub
import os
from global_variables import FINNHUB_TOKEN, SYMBOL

finnhub_client = finnhub.Client(api_key=FINNHUB_TOKEN)

def fetch_sentiment_data():
    news = finnhub_client.company_news(SYMBOL, _from="2024-07-01", to="2024-07-04")
    positive = [n for n in news if "positive" in n['summary'].lower()]
    negative = [n for n in news if "negative" in n['summary'].lower()]
    summary = f"{len(positive)} positive and {len(negative)} negative news items."
    return {
        "summary": summary,
        "raw_news": news[:3]  # limit for brevity
    }

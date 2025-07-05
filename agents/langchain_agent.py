#### --- agents/langchain_agent.py ---
# This file contains the LangChain agent that processes stock price anomalies using LLMs.
from langchain_community.llms import Ollama
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama3:3.2b")

def respond_to_anomaly(data):
    template = """You are a financial analyst. Explain the significance of a price change in {symbol} stock.\nCurrent price: ${price}\nTimestamp: {timestamp}\nIs this anomaly possibly related to broader market events?"""
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(symbol=data['symbol'], price=data['price'], timestamp=data['timestamp'])
    print("\n📢 Agent Response:\n", response)


## ---------------- utils/data_processing.py ----------------
# Reserved for advanced preprocessing, e.g., smoothing, normalization

def normalize_price(price):
    return round(price, 2)
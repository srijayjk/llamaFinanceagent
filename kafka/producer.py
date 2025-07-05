import json
import time
import yaml
import os
import logging
import finnhub
from kafka import KafkaProducer
import prometheus_client
from prometheus_client import Counter, Gauge
from global_variables import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, FINNHUB_TOKEN, SYMBOL

# --- Start Prometheus metrics server on port 8000 ---
try:
    prometheus_client.start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
except Exception as e:
    print(f"Failed to start Prometheus metrics server: {e}. Exiting.")
    exit(1)

# --- Define Prometheus metrics ---
STOCK_PRICE_GAUGE = Gauge(
    'stock_current_price',
    'Current stock price of the symbol.',
    ['symbol']
)

PRICE_FETCH_COUNT = Counter(
    'stock_price_fetch_total',
    'Total number of successful stock price fetches.',
    ['symbol']
)

API_ERROR_COUNT = Counter(
    'stock_api_errors_total',
    'Total number of Finnhub API errors.',
    ['symbol']
)

ANOMALY_COUNT = Counter("anomaly_count_total", "Total anomalies detected")

# --- Initialize Kafka producer ---
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )
    print(f"Kafka producer initialized for topic: {KAFKA_TOPIC} on {KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    print(f"Failed to initialize Kafka producer: {e}. Exiting.")
    exit(1)

# --- Initialize Finnhub client ---
finnhub_client = finnhub.Client(api_key=FINNHUB_TOKEN)

def fetch_stock_price():
    try:
        quote = finnhub_client.quote(SYMBOL)
        # quote dict keys: c = current price, h = high price, l = low price, o = open price, pc = previous close price, t = timestamp
        if 'c' in quote and quote['c'] is not None:
            return quote['c']
        else:
            print(f"Invalid quote data: {quote}")
            API_ERROR_COUNT.labels(symbol=SYMBOL).inc()
            return None
    except Exception as e:
        print(f"Exception fetching stock price for {SYMBOL}: {e}")
        API_ERROR_COUNT.labels(symbol=SYMBOL).inc()
        return None

# --- Main loop ---
if __name__ == '__main__':
    print("Starting stock data production loop...")
    while True:
        current_price = fetch_stock_price()

        if current_price is not None:
            event = {
                "symbol": SYMBOL,
                "timestamp": time.time(),
                "price": round(current_price, 2)
            }
            print(f"Produced: {json.dumps(event)}")

            # Update Prometheus metrics
            STOCK_PRICE_GAUGE.labels(symbol=SYMBOL).set(current_price)
            PRICE_FETCH_COUNT.labels(symbol=SYMBOL).inc()

            try:
                future = producer.send(KAFKA_TOPIC, event)
                record_metadata = future.get(timeout=10)
                print(f"Message sent to topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")
            except Exception as e:
                print(f"Failed to send message to Kafka: {e}. Event: {event}")
        else:
            print(f"Could not get valid current price for {SYMBOL}. Skipping Kafka production.")
            # ANOMALY_COUNT.inc()  # Uncomment if you want to count this as anomaly

        time.sleep(5)

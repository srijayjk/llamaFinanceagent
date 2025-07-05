from kafka import KafkaConsumer
import json
import yaml
from collections import deque
from langgraph_pipeline.graph_builder import graph

config = yaml.safe_load(open("config/settings.yaml"))
consumer = KafkaConsumer(
    config['kafka']['topic'],
    bootstrap_servers=config['kafka']['bootstrap_servers'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

window = deque(maxlen=30)

for message in consumer:
    data = message.value
    print(f"Consumed: {data}")
    window.append(data['price'])

    if len(window) >= 30:
        state = {
            "symbol": data['symbol'],
            "prices": list(window)
        }
        result = graph.invoke(state)

        print("\n📊 Forecast:", result['forecast'])
        print("🧠 Sentiment:", result['sentiment'])
        print("💬 Explanation:\n", result['explanation'])

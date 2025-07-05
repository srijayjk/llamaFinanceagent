# llamaFinanceagent



Use memory to track last 10 prices → detect price jumps

📉 Compare to moving averages

📬 Send anomaly alerts to email/Slack

📈 Use a database or dashboard to log agent judgments



📉 Detect unusual price movement

⚠️ Identify suspicious trading patterns

💬 Explain market news in natural language

🧠 Suggest probable causes (earnings, news, etc.)


| Component              | Purpose                                     |
| ---------------------- | ------------------------------------------- |
| **Finnhub.io**         | Real-time financial data source             |
| **Kafka**              | Streaming data pipeline (producer/consumer) |
| **LangChain + Ollama** | Agent-based reasoning for anomaly detection |
| **Python**             | Primary orchestration language              |



[financial-anomaly-detector/
│
├── config/
│   └── settings.yaml
├── kafka/
│   ├── producer.py
│   └── consumer.py
├── agent/
│   ├── anomaly_detector.py
│   └── langchain_agent.py
├── utils/
│   └── data_processing.py
├── main.py
├── requirements.txt
└── README.md](url)


## requirements.txt
```bash
kafka-python
requests
langchain
ollama
python-dotenv
```

## Code Structure
 -> docker-compose.yml — orchestrates Kafka, Zookeeper, Prometheus, Grafana, Kafka Exporter
 -> config/ — configuration files for Prometheus and Grafana dashboards
 -> kafka/producer.py — reads Finnhub API, publishes price messages to Kafka
 -> kafka/consumer.py — consumes price data, runs anomaly detection, increments Prometheus counters



### Troubleshooting Tips
Kafka not connecting?
Make sure Kafka container is up and port 9092 is reachable.

Prometheus config mount errors?
Confirm file paths and permissions on config/prometheus.yml.

Consumer says NoBrokersAvailable?
Double-check Kafka bootstrap servers and ensure Kafka is running.

agent/langchain_agent.py — LangChain + Ollama logic for anomaly reasoning

agent/anomaly_detector.py — defines anomaly detection logic




## Future Enhancements
Add automated alerts (Slack/email) on anomalies.

More complex anomaly detection models.

Persist anomaly events to a database.

Add historical price data analysis.

Scale with Kafka partitions and consumer groups.
requirements.txt — python dependencies


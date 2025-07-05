## ---------------- main.py ----------------
import subprocess
import threading
import time
import os
import signal
import sys
import yaml
from kafka.admin import KafkaAdminClient
from kafka.errors import NoBrokersAvailable

# Function to read config from file (assuming config/settings.yaml is relative to main.py)
def load_config():
    try:
        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'config', 'settings.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Could not load config/settings.yaml: {e}")
        sys.exit(1)

def wait_for_kafka(bootstrap_servers, timeout=60, interval=5):
    print(f"Waiting for Kafka to be ready at {bootstrap_servers}...")
    start_time = time.time()
    while True:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            admin_client.close()
            print("Kafka is ready!")
            return True
        except NoBrokersAvailable:
            print(f"Kafka not yet available at {bootstrap_servers}. Retrying in {interval}s...")
            time.sleep(interval)
        except Exception as e:
            print(f"An unexpected error occurred while waiting for Kafka: {e}. Retrying in {interval}s...")
            time.sleep(interval)

        if time.time() - start_time > timeout:
            print(f"ERROR: Kafka did not become ready within {timeout} seconds. Exiting.")
            return False

def run_script_in_background(script_path):
    process = subprocess.Popen(["python", script_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                bufsize=1)

    def log_output(stream, prefix):
        for line in stream:
            print(f"[{prefix}] {line.strip()}")

    threading.Thread(target=log_output, args=(process.stdout, os.path.basename(script_path)), daemon=True).start()
    threading.Thread(target=log_output, args=(process.stderr, f"{os.path.basename(script_path)} ERROR"), daemon=True).start()

    return process


def main():
    print("🚀 Starting Financial Anomaly Detector stack...")

    config = load_config()
    kafka_bootstrap_servers = config['kafka']['bootstrap_servers']

    # Wait for Kafka to be ready
    if not wait_for_kafka(kafka_bootstrap_servers):
        print("Exiting due to Kafka not being ready.")
        sys.exit(1)

    processes = []

    # Start consumer (assuming kafka/consumer.py exists)
    consumer_process = run_script_in_background("kafka/consumer.py")
    processes.append(consumer_process)
    print(f"Started consumer (PID: {consumer_process.pid})")

    # Give some time for consumer to initialize (optional, can be removed if consumer is robust)
    time.sleep(3)

    # Start producer
    producer_process = run_script_in_background("kafka/producer.py")
    processes.append(producer_process)
    print(f"Started producer (PID: {producer_process.pid})")

    print("\nAll application components started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Shutting down application components...")
        for p in processes:
            if p.poll() is None:
                print(f"Terminating process {p.args} (PID: {p.pid})...")
                p.terminate()
                p.wait(timeout=5)
                if p.poll() is None:
                    print(f"Process {p.args} (PID: {p.pid}) did not terminate gracefully. Killing...")
                    p.kill()

    print("Application components shut down.")


if __name__ == '__main__':
    main()
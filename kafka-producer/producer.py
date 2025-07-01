from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time
import random

from data_generators.employee import EmployeeGenerator
from data_generators.department import DepartmentGenerator
from data_generators.project import ProjectGenerator
from data_generators.salary import SalaryGenerator
from data_generators.attendance import AttendanceGenerator

# === Kafka Setup ===
def setup_producer():
    producer = None
    for i in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka!")
            return producer
        except NoBrokersAvailable:
            print(f"❌ Kafka not available (attempt {i+1}/10). Retrying in 5s...")
            time.sleep(5)

    raise Exception("❌ Failed to connect to Kafka after retries.")

# === Main Producer Logic ===
def main():
    producer = setup_producer()

    topics = {
        "employees": EmployeeGenerator,
        "departments": DepartmentGenerator,
        "projects": ProjectGenerator,
        "salaries": SalaryGenerator,
        "attendance": AttendanceGenerator
    }

    while True:
        topic = random.choice(list(topics.keys()))
        data = topics[topic].generate()
        producer.send(topic, value=data)
        print(f"📤 Sent to {topic}: {data}")
        time.sleep(2)

if __name__ == "__main__":
    main()
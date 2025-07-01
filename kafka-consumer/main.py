from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient, errors as mongo_errors
import json
import time

# === Config ===
TOPICS = ["employees", "departments", "projects", "salaries", "attendance"]
MONGO_DB_NAME = "employee_data"

# === Retry Kafka connection ===
consumer = None
for i in range(10):
    try:
        print(f"[Kafka] Attempting to connect (try {i+1}/10)...")
        consumer = KafkaConsumer(
            *TOPICS,
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='employee-group',
            auto_offset_reset='earliest'
        )
        print("✅ Connected to Kafka!")
        break
    except NoBrokersAvailable:
        print(f"❌ Kafka not available (attempt {i+1}/10). Retrying in 5s...")
        time.sleep(5)

if not consumer:
    raise Exception("❌ Failed to connect to Kafka after retries.")

# === Retry MongoDB connection ===
client = None
for i in range(10):
    try:
        print(f"[MongoDB] Attempting to connect (try {i+1}/10)...")
        client = MongoClient("mongodb", 27017, serverSelectionTimeoutMS=2000)
        client.server_info()  # Force connection
        print("✅ Connected to MongoDB!")
        break
    except mongo_errors.ServerSelectionTimeoutError:
        print(f"❌ MongoDB not available (attempt {i+1}/10). Retrying in 5s...")
        time.sleep(5)

if not client:
    raise Exception("❌ Failed to connect to MongoDB after retries.")

# === Select DB ===
db = client[MONGO_DB_NAME]

# === Consume from Kafka and write to Mongo ===
print("🚀 Started consuming messages from topics:", TOPICS)
for message in consumer:
    topic = message.topic
    value = message.value

    print(f"\n📥 [Topic: {topic}] Received message: {value}")

    try:
        collection = db[topic]  # Collection named same as topic
        result = collection.insert_one(value)
        print(f"💾 Inserted into collection `{topic}` with _id: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Failed to insert into `{topic}` collection: {e}")

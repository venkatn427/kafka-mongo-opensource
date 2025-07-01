import time
from pymongo import MongoClient
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# MongoDB connection string (adjust as needed)
MONGO_URI = "mongodb://mongodb:27017"

# PostgreSQL connection parameters
POSTGRES_CONN_INFO = {
    "host": "postgres",       # must be reachable from script's environment
    "port": 5432,
    "user": "superset",
    "password": "superset",
    "dbname": "superset"
}

def create_metrics_table():
    """Create metrics table if it doesn't exist."""
    with psycopg2.connect(**POSTGRES_CONN_INFO) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    metric_name TEXT PRIMARY KEY,
                    metric_value INTEGER,
                    updated_at TIMESTAMP
                );
            """)
        conn.commit()

def fetch_metrics_from_mongo():
    """Query MongoDB to count documents for metrics."""
    client = MongoClient(MONGO_URI)
    db = client.events_db

    num_employees = db.employees.count_documents({})
    num_departments = db.departments.count_documents({})

    return [
        ("num_employees", num_employees, datetime.utcnow()),
        ("num_departments", num_departments, datetime.utcnow()),
    ]

def upsert_metrics_to_postgres(metrics):
    """Insert or update metrics into Postgres."""
    with psycopg2.connect(**POSTGRES_CONN_INFO) as conn:
        with conn.cursor() as cur:
            upsert_sql = """
            INSERT INTO metrics (metric_name, metric_value, updated_at)
            VALUES %s
            ON CONFLICT (metric_name)
            DO UPDATE SET
                metric_value = EXCLUDED.metric_value,
                updated_at = EXCLUDED.updated_at;
            """
            execute_values(cur, upsert_sql, metrics)
        conn.commit()

if __name__ == "__main__":
    create_metrics_table()

    while True:
        try:
            metrics = fetch_metrics_from_mongo()
            upsert_metrics_to_postgres(metrics)
            print(f"[metrics-loader] Updated metrics: {metrics}")
        except Exception as e:
            print(f"[metrics-loader] ERROR: {e}")
        time.sleep(30)

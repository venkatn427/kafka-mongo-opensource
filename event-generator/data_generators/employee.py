import random
from datetime import datetime, timedelta

first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward"]
last_names = ["Smith", "Johnson", "Lee", "Patel", "Brown"]
departments = ["Engineering", "HR", "Sales", "Marketing", "Finance"]

class EmployeeGenerator:
    @staticmethod
    def generate():
        return {
            "employee_id": random.randint(1000, 9999),
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "department": random.choice(departments),
            "date_joined": (datetime.now() - timedelta(days=random.randint(30, 2000))).strftime("%Y-%m-%d")
        }

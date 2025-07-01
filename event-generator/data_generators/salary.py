import random
from datetime import datetime

class SalaryGenerator:
    @staticmethod
    def generate():
        return {
            "employee_id": random.randint(1000, 9999),
            "base": round(random.uniform(40000, 120000), 2),
            "bonus": round(random.uniform(1000, 10000), 2),
            "effective_date": datetime.now().strftime("%Y-%m-%d")
        }

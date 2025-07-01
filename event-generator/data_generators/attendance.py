import random
from datetime import datetime

class AttendanceGenerator:
    @staticmethod
    def generate():
        return {
            "employee_id": random.randint(1000, 9999),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": random.choice(["Present", "Absent", "Remote", "Leave"])
        }

import random
from data_generators.employee import first_names, last_names, departments

class DepartmentGenerator:
    @staticmethod
    def generate():
        return {
            "department_id": random.randint(10, 99),
            "name": random.choice(departments),
            "manager": f"{random.choice(first_names)} {random.choice(last_names)}"
        }

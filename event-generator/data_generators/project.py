import random
from data_generators.employee import departments

projects = ["Apollo", "Zeus", "Hermes", "Athena", "Poseidon"]

class ProjectGenerator:
    @staticmethod
    def generate():
        return {
            "project_id": random.randint(100, 199),
            "name": random.choice(projects),
            "budget": round(random.uniform(50000, 500000), 2),
            "department": random.choice(departments)
        }

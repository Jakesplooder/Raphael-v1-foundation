import os
import json
import logging

logger = logging.getLogger("rrk.workforce.memory")

class EmployeeMemory:
    """
    Individual memory for each employee.
    
    Structure:
    base_dir/employees/<employee_id>/
        experiences.json
        mistakes.json
        successful_patterns.json
        learned_skills.json
    """
    
    def __init__(self, base_dir="workforce_memory"):
        self.base_dir = base_dir
        self.categories = ["experiences", "mistakes", "successful_patterns", "learned_skills"]
        
    def setup_employee(self, employee_id: str):
        emp_dir = os.path.join(self.base_dir, "employees", employee_id)
        os.makedirs(emp_dir, exist_ok=True)
        for cat in self.categories:
            file_path = os.path.join(emp_dir, f"{cat}.json")
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    json.dump([], f)
                    
    def record(self, employee_id: str, category: str, entry: dict):
        if category not in self.categories:
            logger.error(f"Invalid memory category: {category}")
            return
            
        file_path = os.path.join(self.base_dir, "employees", employee_id, f"{category}.json")
        data = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        data.append(entry)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Recorded {category} for employee {employee_id}")
        
    def recall(self, employee_id: str, category: str) -> list:
        file_path = os.path.join(self.base_dir, "employees", employee_id, f"{category}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return []

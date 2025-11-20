import sqlite3
from typing import List, Tuple, Dict

class DataQualityTester:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    def check_duplicates(self) -> List[Tuple]:
        """Sprawdza duplikaty w tabeli employees"""
        query = """
        SELECT first_name, last_name, COUNT(*) as count 
        FROM employees 
        GROUP BY first_name, last_name 
        HAVING COUNT(*) > 1
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def check_nulls_employees(self) -> List[Tuple]:
        """Sprawdza NULL wartości w tabeli employees"""
        query = """
        SELECT * FROM employees 
        WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL 
        OR dept_id IS NULL OR salary IS NULL OR hire_date IS NULL
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def check_foreign_key_violations(self) -> List[Tuple]:
        """Sprawdza naruszenia kluczy obcych"""
        query = """
        SELECT * FROM employees 
        WHERE dept_id NOT IN (SELECT dept_id FROM departments WHERE dept_id IS NOT NULL)
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def check_salary_budget_violations(self) -> List[Tuple]:
        """Sprawdza czy suma pensji przekracza budżet działu"""
        query = """
        SELECT d.dept_name, d.budget, SUM(e.salary) as total_salaries
        FROM departments d
        JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name, d.budget
        HAVING SUM(e.salary) > d.budget
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def check_unreasonable_salaries(self) -> List[Tuple]:
        """Sprawdza nierozsądne pensje (poza zakresem 0-10000)"""
        query = """
        SELECT first_name, last_name, salary 
        FROM employees 
        WHERE salary < 0 OR salary > 10000
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def check_future_hire_dates(self) -> List[Tuple]:
        """Sprawdza daty zatrudnienia z przyszłości"""
        query = """
        SELECT first_name, last_name, hire_date 
        FROM employees 
        WHERE hire_date > CURRENT_DATE
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_data_quality_summary(self) -> Dict[str, int]:
        """Zwraca podsumowanie wszystkich problemów z jakością danych"""
        return {
            'duplicates': len(self.check_duplicates()),
            'nulls': len(self.check_nulls_employees()),
            'foreign_key_violations': len(self.check_foreign_key_violations()),
            'budget_violations': len(self.check_salary_budget_violations()),
            'unreasonable_salaries': len(self.check_unreasonable_salaries()),
            'future_hire_dates': len(self.check_future_hire_dates())
        }
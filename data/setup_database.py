import sqlite3
import os

def create_database():
    # Create database file
    db_path = os.path.join(os.path.dirname(__file__), 'test_database.db')
    
    # Table names
    table_names = ['departments', 'employees']
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create departments table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_names[0]} (
            dept_id INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL,
            location TEXT,
            budget DECIMAL(10,2)
        )
    ''')
    
    # Create employees table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_names[1]} (
            emp_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            dept_id INTEGER,
            salary DECIMAL(10,2),
            hire_date DATE,
            FOREIGN KEY (dept_id) REFERENCES {table_names[0]} (dept_id)
        )
    ''')
    
    # Insert sample departments
    departments_data = [
        (1, 'IT', 'Warsaw', 500000.00),
        (2, 'HR', 'Krakow', 200000.00),
        (3, 'Finance', 'Warsaw', 300000.00),
        (4, 'Marketing', None, 150000.00),  # NULL location for testing
    ]
    
    cursor.executemany(f'''
        INSERT OR REPLACE INTO {table_names[0]} (dept_id, dept_name, location, budget)
        VALUES (?, ?, ?, ?)
    ''', departments_data)
    
    # Insert sample employees (with some data quality issues)
    employees_data = [
        (1, 'Jan', 'Kowalski', 'jan.kowalski@company.com', 1, 8000.00, '2023-01-15'),
        (2, 'Anna', 'Nowak', 'anna.nowak@company.com', 2, 6500.00, '2023-02-20'),
        (3, 'Piotr', 'Wiśniewski', 'piotr.wisniewski@company.com', 1, 7500.00, '2023-03-10'),
        (4, 'Maria', None, 'maria@company.com', 3, 9000.00, '2023-01-05'),  # NULL last_name
        (5, 'Tomasz', 'Kowalczyk', None, 2, 5500.00, '2023-04-12'),  # NULL email
        (6, 'Jan', 'Kowalski', 'jan.kowalski@company.com', 1, 8000.00, '2023-01-15'),  # Duplicate
        (7, 'Katarzyna', 'Zielińska', 'katarzyna.zielinska@company.com', 5, 7000.00, '2023-05-01'),  # Invalid dept_id
    ]
    
    cursor.executemany(f'''
        INSERT OR REPLACE INTO {table_names[1]} (emp_id, first_name, last_name, email, dept_id, salary, hire_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print(f"Tables created: {', '.join(table_names)}")
    print("Sample data inserted with intentional quality issues for testing")

if __name__ == "__main__":
    create_database()
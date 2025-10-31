import sqlite3

def view_database():
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    
    print("=== TABLES ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    
    print("\n=== DEPARTMENTS ===")
    cursor.execute("SELECT * FROM departments")
    for row in cursor.fetchall():
        print(row)
    
    print("\n=== EMPLOYEES ===")
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

if __name__ == "__main__":
    view_database()
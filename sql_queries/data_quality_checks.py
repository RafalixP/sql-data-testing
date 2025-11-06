import sqlite3

def find_duplicates(cursor):
    print("\n=== szukamy duplikatów ===")
    cursor.execute("select first_name, last_name, count(last_name) AS licznik from employees group by first_name, last_name having licznik > 1")
    for row in cursor.fetchall():
        print(row)

def find_nulls(cursor):
    print("\n=== szukamy NULLi:")
    print("===Tabela Departments - rekordy zawierające puste komórki:")
    cursor.execute("SELECT * FROM departments WHERE dept_name IS NULL OR location IS NULL OR budget IS NULL")
    for row in cursor.fetchall():
        print(row)

    print("\n===Tabela Employees - rekordy zawierające puste komórki:")
    cursor.execute("SELECT * FROM employees WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL OR dept_id IS NULL OR salary IS NULL OR hire_date IS NULL")
    for row in cursor.fetchall():
        print(row)

def key_violations(cursor):
    print("\n=== szukamy błednych kluczy obcych - opcja 1 left join===")
    cursor.execute("SELECT employees.*, departments.dept_name FROM employees LEFT JOIN departments ON employees.dept_id = departments.dept_id WHERE departments.dept_id IS NULL")
    for row in cursor.fetchall():
        print(row)

    print("\n=== szukamy błednych kluczy obcych - opcja 2 not exists===")
    cursor.execute("SELECT * FROM employees WHERE NOT EXISTS (    SELECT 1 FROM departments     WHERE departments.dept_id = employees.dept_id)")
    for row in cursor.fetchall():
        print(row)

    print("\n=== szukamy błednych kluczy obcych - opcja 3 simple===")
    cursor.execute("SELECT * FROM employees WHERE dept_id NOT IN (SELECT dept_id FROM departments)")
    for row in cursor.fetchall():
        print(row)

def run_all_checks():
    conn = sqlite3.connect('../data/test_database.db')
    cursor = conn.cursor()

    print('\nRunning all of the data quality checks:')
    find_duplicates(cursor)
    find_nulls(cursor)
    key_violations(cursor)

    print()
    
    conn.close()

if __name__ == "__main__":
    run_all_checks()




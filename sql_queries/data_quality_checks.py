import sqlite3
from tabulate import tabulate

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
        
    print("\n===Tabela Employees - rekordy zawierające puste komórki wersja 2:")
    cursor.execute("SELECT *, 'first_name' as null_column FROM employees WHERE first_name IS NULL UNION ALL SELECT *, 'last_name' as null_column FROM employees WHERE last_name IS NULL UNION ALL SELECT *, 'email' as null_column FROM employees WHERE email IS NULL UNION ALL SELECT *, 'dept_id' as null_column FROM employees WHERE dept_id IS NULL UNION ALL SELECT *, 'salary' as null_column FROM employees WHERE salary IS NULL UNION ALL SELECT *, 'hire_date' as null_column FROM employees WHERE hire_date IS NULL")
    for row in cursor.fetchall():
        print(row)

    print("\n===Tabela Employees - rekordy zawierające puste komórki wersja 3:")
    cursor.execute("SELECT *, CASE WHEN first_name IS NULL THEN 'first_name, ' ELSE '' END || CASE WHEN last_name IS NULL THEN 'last_name, ' ELSE '' END || CASE WHEN email IS NULL THEN 'email, ' ELSE '' END || CASE WHEN dept_id IS NULL THEN 'dept_id, ' ELSE '' END || CASE WHEN salary IS NULL THEN 'salary, ' ELSE '' END || CASE WHEN hire_date IS NULL THEN 'hire_date' ELSE '' END as null_columns FROM employees WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL OR dept_id IS NULL OR salary IS NULL OR hire_date IS NULL")
    for row in cursor.fetchall():
        print(row)

    print("\n===Tabela Employees - rekordy zawierające puste komórki wersja 4:")
    cursor.execute("SELECT *, 'Critical NULL' as issue_type FROM employees WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL UNION ALL SELECT *, 'Minor NULL' as issue_type FROM employees WHERE dept_id IS NULL OR salary IS NULL OR hire_date IS NULL")
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

def salary_consistency(cursor):
    print("\n=== sprawdzamy czy suma pensji pracowników w działach nie przekracza budżetu działów ===")
    cursor.execute("SELECT dept_name, employees.dept_id, sum(employees.salary) AS sum_of_salaries, budget, budget-sum(employees.salary) AS difference, CASE WHEN budget-sum(employees.salary) >= 0 THEN 'mieścimy się w budżecie' ELSE 'budżet przekroczony' END AS budget_status FROM employees JOIN departments ON employees.dept_id = departments.dept_id GROUP BY employees.dept_id, dept_name, budget")
    
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))
    #for row in cursor.fetchall():
    #    print(row)

def is_salary_reasonable(cursor):
    print("\n === Sprawdzamy czy pensje pracowników można uznać za sensowne ===")
    cursor.execute("SELECT first_name, last_name, salary, CASE WHEN salary BETWEEN 0 AND 6000 THEN 'pensja jest rozsądna' ELSE 'pensja jest nierozsądna' END AS Opinia_o_pensji FROM employees")

    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

def is_hire_date_correct(cursor):
    print("\n=== sprawdzamy czy daty zatrudnienia są poprawne, tzn. czy nie są z przyszłości")

    cursor.execute("SELECT first_name, last_name, hire_date, CASE WHEN hire_date <= CURRENT_DATE THEN 'data zatrudnienia jest prawidłowa' ELSE 'jest problem z datą zatrudnienia' END AS Czy_data_jest_OK FROM employees")
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

def is_department_empty(cursor):
    print("\n=== Lista działów które mają / nie mają pracowników ===")

    print("\n Mają ")
    cursor.execute("select * from departments where dept_id IN (select dept_id from employees WHERE dept_id IS NOT NULL)")
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

    print("\n Nie mają ")
    cursor.execute("select * from departments where dept_id NOT IN (select dept_id from employees WHERE dept_id IS NOT NULL)")
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))    

    print("\n Wszystkie działy ze statusem ")
    cursor.execute("select *, CASE WHEN dept_id NOT IN (select dept_id from employees WHERE dept_id IS NOT NULL) THEN 'dział bez pracownika' ELSE 'dział z pracownikami' END AS 'Status_działu' from departments")
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

    print("\n=== Data Quality Dashboard - wszystkie metryki ===")
    cursor.execute("""
        SELECT 
            'Duplicates' as check_type,
            COUNT(*) as issues_found,
            'Critical' as severity
        FROM (SELECT first_name, last_name FROM employees GROUP BY first_name, last_name HAVING COUNT(*) > 1)

        UNION ALL

        SELECT 
            'NULL Values' as check_type,
            COUNT(*) as issues_found,
            'High' as sevty  
        FROM employees WHERE first_name IS NULL OR last_name IS NULL OR email IS NULL

        UNION ALL

        SELECT 
            'Orphaned Records' as type,
            COUNT(*) as issues_found,
            'Critical' as severity
        FROM employees WHERE dept_id NOT IN (SELECT dept_id FROM departments WHERE dept_id IS NOT NULL)
    """)
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

    print("\n=== Employee Health Report - kompleksowa analiza pracowników ===")
    cursor.execute("""
        SELECT 
            e.first_name,
            e.last_name,
            e.salary,
            d.dept_name,
            CASE WHEN e.first_name IS NULL OR e.last_name IS NULL THEN 'Missing Name' ELSE 'OK' END as name_status,
            CASE WHEN e.salary BETWEEN 0 AND 10000 THEN 'OK' ELSE 'Suspicious Salary' END as salary_status,
            CASE WHEN e.dept_id IN (SELECT dept_id FROM departments WHERE dept_id IS NOT NULL) THEN 'Valid Dept' ELSE 'Invalid Dept' END as dept_status
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
    """)
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))

    print("\n=== Cross-Table Reconciliation - porównanie sum między tabelami ===")
    cursor.execute("""
        SELECT 
            'Total Employees' as metric,
            COUNT(*) as employee_count,
            (SELECT COUNT(DISTINCT dept_id) FROM departments) as dept_count,
            ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM departments), 2) as avg_employees_per_dept
        FROM employees
    """)
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    print(tabulate(results, headers=columns, tablefmt="grid"))  


def run_all_checks():
    conn = sqlite3.connect('../data/test_database.db')
    cursor = conn.cursor()

    print('\nRunning all of the data quality checks:')
    find_duplicates(cursor)
    find_nulls(cursor)
    key_violations(cursor)
    salary_consistency(cursor)
    is_salary_reasonable(cursor)
    is_hire_date_correct(cursor)
    is_department_empty(cursor)

    print()
    
    conn.close()

if __name__ == "__main__":
    run_all_checks()




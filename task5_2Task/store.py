import mysql.connector
from mysql.connector import Error
import csv

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904"
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS store_db")
    cursor.execute("USE store_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            city VARCHAR(255)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255),
            price FLOAT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    customers = [
        ('Alice', 'New York'),
        ('Bob', 'Chicago'),
        ('Charlie', 'Boston'),
        ('David', 'Dallas'),
        ('Eva', 'Seattle'),
        ('Frank', 'Denver'),
        ('Grace', 'Miami'),
        ('Henry', 'Phoenix'),
        ('Ivy', 'Austin'),
        ('Jack', 'Atlanta')
    ]

    products = [
        ('Laptop', 1200),
        ('Phone', 800),
        ('Tablet', 500),
        ('Monitor', 300),
        ('Keyboard', 100),
        ('Mouse', 50),
        ('Printer', 250),
        ('Speaker', 150)
    ]

    orders = [
        (1, 1, 2, '2025-05-01'),
        (1, 2, 1, '2025-05-02'),
        (2, 3, 3, '2025-05-03'),
        (2, 4, 1, '2025-05-04'),
        (3, 1, 1, '2025-05-05'),
        (3, 5, 4, '2025-05-06'),
        (4, 6, 5, '2025-05-07'),
        (4, 2, 2, '2025-05-08'),
        (5, 3, 1, '2025-05-09'),
        (5, 7, 1, '2025-05-10'),
        (6, 8, 2, '2025-05-11'),
        (6, 1, 1, '2025-05-12'),
        (7, 2, 3, '2025-05-13'),
        (7, 5, 2, '2025-05-14'),
        (8, 4, 1, '2025-05-15'),
        (8, 6, 6, '2025-05-16'),
        (9, 7, 2, '2025-05-17'),
        (9, 3, 2, '2025-05-18'),
        (10, 8, 1, '2025-05-19'),
        (10, 1, 1, '2025-05-20')
    ]

    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO customers (name, city)
            VALUES (%s, %s)
        """, customers)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO products (product_name, price)
            VALUES (%s, %s)
        """, products)

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO orders (customer_id, product_id, quantity, order_date)
            VALUES (%s, %s, %s, %s)
        """, orders)

    conn.commit()

    print("\nTotal Money Spent Per Customer")

    cursor.execute("""
        SELECT c.name,
               SUM(p.price * o.quantity) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        GROUP BY c.name
        ORDER BY total_spent DESC
    """)

    revenue_rows = cursor.fetchall()

    print(f"{'Customer':<15} {'Total Spent'}")
    print("-" * 30)

    for row in revenue_rows:
        print(f"{row[0]:<15} {row[1]}")

    print("\nMost Ordered Product By Quantity")

    cursor.execute("""
        SELECT p.product_name,
               SUM(o.quantity) AS total_quantity
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    print(f"Product: {row[0]}")
    print(f"Total Quantity Ordered: {row[1]}")

    print("\nCustomers With More Than 2 Orders")

    cursor.execute("""
        SELECT c.name,
               COUNT(o.order_id) AS total_orders
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.name
        HAVING COUNT(o.order_id) > 2
    """)

    rows = cursor.fetchall()

    print(f"{'Customer':<15} {'Orders'}")
    print("-" * 25)

    for row in rows:
        print(f"{row[0]:<15} {row[1]}")

    print("\nAverage Order Value Per City")

    cursor.execute("""
        SELECT c.city,
               AVG(p.price * o.quantity) AS avg_order_value
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        GROUP BY c.city
    """)

    rows = cursor.fetchall()

    print(f"{'City':<15} {'Average Order Value'}")
    print("-" * 40)

    for row in rows:
        print(f"{row[0]:<15} {round(row[1], 2)}")

    with open("revenue_report.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Customer", "Total Spent"])

        for row in revenue_rows:
            writer.writerow(row)

    print("\nrevenue_report.csv exported successfully")

    cursor.close()
    conn.close()

except Error as e:
    print(f"Database Error: {e}")
import mysql.connector
from mysql.connector import Error

# ─── Step 1: Create the database ───────────────────────────────────────────────
try:
    setup_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904"
    )
    setup_cursor = setup_conn.cursor()
    setup_cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    print(" Database ready.")
    setup_cursor.close()
    setup_conn.close()

except Error as e:
    print(f" Failed to create database: {e}")
    exit()

# ─── Step 2: Connect to library_db ─────────────────────────────────────────────
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904",
        database="library_db"
    )
    cursor = conn.cursor()
    print(" Connected to library_db.")

except Error as e:
    print(f" Connection failed: {e}")
    exit()

# ─── Step 3: Create table ───────────────────────────────────────────────────────
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INT NOT NULL,
            genre VARCHAR(255) NOT NULL,
            rating FLOAT NOT NULL
        )
    """)
    print(" Table ready.")

except Error as e:
    print(f" Failed to create table: {e}")
    exit()

# ─── Step 4: Insert data (only if table is empty) ──────────────────────────────
data = [
    ('Dune', 'Frank Herbert', 1965, 'Sci-Fi', 4.5),
    ('The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy', 4.7),
    ('1984', 'George Orwell', 1949, 'Dystopian', 4.6),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Classic', 4.0),
    ('The Night Circus', 'Erin Morgenstern', 2011, 'Fantasy', 4.2),
    ('Educated', 'Tara Westover', 2018, 'Memoir', 4.4),
    ('The Midnight Library', 'Matt Haig', 2020, 'Fiction', 4.1),
    ('Dune Messiah', 'Frank Herbert', 1969, 'Sci-Fi', 4.3)
]

try:
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
            INSERT INTO books (title, author, year, genre, rating)
            VALUES (%s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        print(f" Inserted {cursor.rowcount} rows.")
    else:
        print(f"ℹ  Table already has {count} rows, skipping insert.")

except Error as e:
    print(f" Insert failed: {e}")
    exit()

# ─── Step 5: Query 1 — Books after 2000, sorted by rating ──────────────────────
try:
    cursor.execute("SELECT * FROM books WHERE year > 2000 ORDER BY rating DESC")
    rows = cursor.fetchall()
    print("\n Books published after 2000:")
    print(f"{'ID':<5} {'Title':<25} {'Author':<25} {'Year':<6} {'Genre':<12} {'Rating'}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<25} {row[3]:<6} {row[4]:<12} {row[5]}")

except Error as e:
    print(f" Query 1 failed: {e}")

# ─── Step 6: Query 2 — Fiction books with rating > 4.0 ─────────────────────────
try:
    cursor.execute("SELECT * FROM books WHERE genre='Fiction' AND rating > 4.0")
    rows = cursor.fetchall()
    print("\n Fiction books with rating > 4.0:")
    print(f"{'ID':<5} {'Title':<25} {'Author':<25} {'Year':<6} {'Genre':<12} {'Rating'}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<25} {row[3]:<6} {row[4]:<12} {row[5]}")

except Error as e:
    print(f" Query 2 failed: {e}")

# ─── Cleanup ────────────────────────────────────────────────────────────────────
cursor.close()
conn.close()
print("\n Done. Connection closed.")
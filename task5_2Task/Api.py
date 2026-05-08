import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

API_URL = "https://jsonplaceholder.typicode.com/posts"

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904"
    )

    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS monitor_db")
        cursor.execute("USE monitor_db")
    except Error as e:
        print(f"Database creation error: {e}")

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT PRIMARY KEY,
                userId INT,
                title TEXT,
                body TEXT
            )
        """)
    except Error as e:
        print(f"Posts table error: {e}")

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS change_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                post_id INT,
                userId INT,
                change_type VARCHAR(50),
                change_time DATETIME
            )
        """)
    except Error as e:
        print(f"Change log table error: {e}")

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            posts = response.json()
        else:
            print("API request failed")
            posts = []

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        posts = []

    current_time = datetime.now()

    for post in posts:

        try:
            cursor.execute("""
                SELECT title, body
                FROM posts
                WHERE id = %s
            """, (post['id'],))

            existing_post = cursor.fetchone()

            if existing_post is None:

                cursor.execute("""
                    INSERT INTO posts (id, userId, title, body)
                    VALUES (%s, %s, %s, %s)
                """, (
                    post['id'],
                    post['userId'],
                    post['title'],
                    post['body']
                ))

                cursor.execute("""
                    INSERT INTO change_log (post_id, userId, change_type, change_time)
                    VALUES (%s, %s, %s, %s)
                """, (
                    post['id'],
                    post['userId'],
                    'NEW',
                    current_time
                ))

            else:

                db_title = existing_post[0]
                db_body = existing_post[1]

                if db_title != post['title'] or db_body != post['body']:

                    cursor.execute("""
                        UPDATE posts
                        SET title = %s,
                            body = %s
                        WHERE id = %s
                    """, (
                        post['title'],
                        post['body'],
                        post['id']
                    ))

                    cursor.execute("""
                        INSERT INTO change_log (post_id, userId, change_type, change_time)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        post['id'],
                        post['userId'],
                        'MODIFIED',
                        current_time
                    ))

        except Error as e:
            print(f"Post processing error: {e}")

    conn.commit()

    print("\nPost Count Per User")

    try:
        cursor.execute("""
            SELECT userId,
                   COUNT(*) AS total_posts
            FROM posts
            GROUP BY userId
        """)

        rows = cursor.fetchall()

        print(f"{'User ID':<10} {'Post Count'}")
        print("-" * 25)

        for row in rows:
            print(f"{row[0]:<10} {row[1]}")

    except Error as e:
        print(f"Query error: {e}")

    print("\nLatest Change Log Entries")

    try:
        cursor.execute("""
            SELECT post_id,
                   userId,
                   change_type,
                   change_time
            FROM change_log
            WHERE DATE(change_time) = CURDATE()
            ORDER BY change_time DESC
        """)

        rows = cursor.fetchall()

        print(f"{'Post ID':<10} {'User ID':<10} {'Type':<15} {'Time'}")
        print("-" * 60)

        for row in rows:
            print(f"{row[0]:<10} {row[1]:<10} {row[2]:<15} {row[3]}")

    except Error as e:
        print(f"Change log query error: {e}")

    print("\nUser With Most Change Events")

    try:
        cursor.execute("""
            SELECT userId,
                   COUNT(*) AS total_changes
            FROM change_log
            GROUP BY userId
            ORDER BY total_changes DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        print(f"User ID: {row[0]}")
        print(f"Total Changes: {row[1]}")

    except Error as e:
        print(f"Analytics query error: {e}")

    cursor.close()
    conn.close()

except Error as e:
    print(f"Connection Error: {e}")
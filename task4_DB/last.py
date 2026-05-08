import requests
import mysql.connector
import pandas as pd
from mysql.connector import Error

API_URL = "https://jsonplaceholder.typicode.com/posts"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Nishan@20640904"
}

DATABASE_NAME = "api_project_db"
TABLE_NAME = "posts"


def create_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

        cursor.close()
        conn.close()

        print("Database ready")

    except Error as e:
        print(f"Database creation failed: {e}")
        exit()


def create_table():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DATABASE_NAME
        )

        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INT PRIMARY KEY,
                userId INT,
                title TEXT,
                body TEXT
            )
        """)

        conn.commit()

        cursor.close()
        conn.close()

        print("Table ready")

    except Error as e:
        print(f"Table creation failed: {e}")
        exit()


def fetch_data():
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()
            print("API data fetched successfully")
            return data
        else:
            print(f"API request failed with status code {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return []


def store_data(data):
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DATABASE_NAME
        )

        cursor = conn.cursor()

        for item in data:

            cursor.execute(f"""
                SELECT * FROM {TABLE_NAME}
                WHERE id = %s
            """, (item["id"],))

            existing = cursor.fetchone()

            if existing:
                print(f"Post ID {item['id']} already exists")
            else:
                cursor.execute(f"""
                    INSERT INTO {TABLE_NAME} (id, userId, title, body)
                    VALUES (%s, %s, %s, %s)
                """, (
                    item["id"],
                    item["userId"],
                    item["title"],
                    item["body"]
                ))

        conn.commit()

        cursor.close()
        conn.close()

        print("Data stored successfully")

    except Error as e:
        print(f"Database insert error: {e}")


def run_report():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DATABASE_NAME
        )

        cursor = conn.cursor()

        print("\nQuery 1: Total Posts")
        cursor.execute(f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
        """)

        total_posts = cursor.fetchone()[0]

        print(f"Total Posts: {total_posts}")

        print("\nQuery 2: Number of Posts Per User")

        cursor.execute(f"""
            SELECT userId, COUNT(*) AS total_posts
            FROM {TABLE_NAME}
            GROUP BY userId
            ORDER BY total_posts DESC
        """)

        rows = cursor.fetchall()

        print(f"{'User ID':<10} {'Total Posts'}")
        print("-" * 25)

        for row in rows:
            print(f"{row[0]:<10} {row[1]}")

        print("\nQuery 3: Posts With Long Titles")

        cursor.execute(f"""
            SELECT id, title
            FROM {TABLE_NAME}
            WHERE LENGTH(title) > 40
        """)

        long_title_rows = cursor.fetchall()

        print(f"{'Post ID':<10} {'Title'}")
        print("-" * 80)

        for row in long_title_rows:
            print(f"{row[0]:<10} {row[1]}")

        export_to_csv(conn)

        cursor.close()
        conn.close()

    except Error as e:
        print(f"Query error: {e}")


def export_to_csv(conn):
    try:
        query = f"""
            SELECT *
            FROM {TABLE_NAME}
        """

        df = pd.read_sql(query, conn)

        df.to_csv("posts_export.csv", index=False)

        with open("posts_export.txt", "w", encoding="utf-8") as file:
            file.write(df.to_string(index=False))

        print("\nData exported successfully")
        print("CSV File: posts_export.csv")
        print("TXT File: posts_export.txt")

    except Exception as e:
        print(f"Export error: {e}")


def main():
    create_database()
    create_table()

    data = fetch_data()

    if data:
        store_data(data)
        run_report()
    else:
        print("No data available")


if __name__ == "__main__":
    main()
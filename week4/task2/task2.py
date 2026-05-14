import pandas as pd
import requests
import mysql.connector

try:

    url = "https://jsonplaceholder.typicode.com/posts"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df[["userId", "id", "title", "body"]]
    print(df.head(100))
    print(df.info())
    print(df.isnull().sum())
    wordcount = df["title"].str.split().str.len()
    df["word_count"] = wordcount
    df = df[df["word_count"] >= 4]
    df["title"] = (
        df["title"]
        .str.strip()
        .str.title()
    )

    df["body"] = (
        df["body"]
        .str.strip()
    )

    df = df.dropna()
    df.to_csv("cleaned_posts.csv", index=False)
    print(f"Total posts before cleaning: {len(data)}")
    print(f"Total posts after cleaning: {len(df)}")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904",
        database="etl_project"
    )

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cleaned_posts (
        userId INT,
        id INT,
        title TEXT,
        body TEXT,
        word_count INT
    )
    """)
    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO cleaned_posts
        (userId, id, title, body, word_count)
        VALUES (%s, %s, %s, %s, %s)
        """, (
            row["userId"],
            row["id"],
            row["title"],
            row["body"],
            row["word_count"]
        ))
    conn.commit()

    print("Data inserted successfully into MySQL")

    print(df.head())

except Exception as e:

    print("Error fetching data:", e)
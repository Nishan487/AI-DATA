import pandas as pd
import requests
import mysql.connector

def analyse_userAnd_post():
    try:
        url = "https://jsonplaceholder.typicode.com/users"
        data = requests.get(url).json()
        df_user = pd.json_normalize(data)
        df_user = df_user[
            ["id", "name", "email", "address.city"]
        ]
        df_user = df_user.rename(
            columns={"address.city": "city"}
        )
        url_post = "https://jsonplaceholder.typicode.com/posts"
        data = requests.get(url_post).json()
        df_post = pd.DataFrame(data)
        df_post = df_post[["userId", "title"]]
        df_post = df_post.rename(
            columns={"userId": "id"}
        )

        merge_df = pd.merge(df_user, df_post, on="id")

        post_count = (
            df_post.groupby("id")
            .size()
            .reset_index(name="post_count")
        )

        df_user = pd.merge(
            df_user,
            post_count,
            on="id"
        )


        df_user["email"] = (
            df_user["email"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        df_user["name"] = (
            df_user["name"]
            .astype(str)
            .str.strip()
        )

        df_user["city"] = (
            df_user["city"]
            .astype(str)
            .str.strip()
        )


        df_user = df_user.dropna()

        merge_df = merge_df.dropna()


        merge_df.to_csv(
            "merged_data.csv",
            index=False
        )


        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nishan@20640904",
            database="etl_project"
        )

        cursor = conn.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS merged_data (
            id INT,
            name VARCHAR(255),
            email VARCHAR(255),
            city VARCHAR(255),
            title TEXT
        )
        """)


        for _, row in merge_df.iterrows():

            cursor.execute("""
            INSERT INTO merged_data
            (id, name, email, city, title)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                row["id"],
                row["name"],
                row["email"],
                row["city"],
                row["title"]
            ))


        conn.commit()

        print("Data inserted successfully")

        print(merge_df.head())


    except Exception as e:

        print("Error:", e)


if __name__ == "__main__":

    analyse_userAnd_post()
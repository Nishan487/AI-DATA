import mysql.connector
from mysql.connector import Error
import dotenv
dotenv.load_dotenv()
import requests
import os

API_KEY = os.getenv("USER_API")
try:
    data=requests.get(API_KEY)
    if data.status_code==200:
        data=data.json()
        for user in data:
            id=user.get('id')
            name=user.get('name')
            email=user.get('email')
            city=user.get('address', {}).get('city')
            phone = user.get("phone")
            
            company_name = user.get('company', {}).get('name')
            # print(f"Name: {name}, Email: {email}, City: {city}")
        
    else:
        print(f"Failed to fetch data,Status code: {data.status_code}")
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904",  
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS USER_DB")
    cursor.close()
    conn.close()
except Error as e:
    print(f"Connection failed: {e}")
    exit()
    
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904",
        database="USER_DB"  
    )
    cursor = conn.cursor()
except Error as e:
    print(f"Connection failed: {e}")
    exit()
    
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            company_name VARCHAR(255) NOT NULL
        )
    """)
except Error as e:
    print(f"Failed to create table: {e}")
    exit()
    
try:
    for user in data:
           
        id=user.get('id')
        name=user.get('name')
        email=user.get('email')
        phone = user.get("phone")
        city=user.get('address',{}).get('city')
        company_name = user.get('company',{}).get('name')
    
    cursor.execute("""
        INSERT INTO users (id, name, email, phone, city, company_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name=VALUES(name),
        email=VALUES(email),
        phone=VALUES(phone),
        city=VALUES(city),
        company_name=VALUES(company_name)
    """, 
    (id, name, email, phone, city, company_name))
    conn.commit()
except Error as e:
    print(f"Failed to insert data: {e}")
    exit()
    
try:
    print("users sort by name:")
    cursor.execute("SELECT * FROM users ORDER BY name ASC")
    for row in cursor.fetchall():
        print(row)
        
    print("\nusers sort/group by city:")
    cursor.execute("SELECT city, COUNT(*) FROM users GROUP BY city HAVING COUNT(*)>1")
    for row in cursor.fetchall():
        print(F"cITY:{row[0]},count:{row[1]}")
        
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT PRIMARY KEY,
                user_id INT,
                title VARCHAR(255),
                body TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # 2. Fetch posts from API
    posts_res = requests.get("https://jsonplaceholder.typicode.com/posts")
    if posts_res.status_code == 200:
        posts_data = posts_res.json()
        
          # 3. Filter and Insert (Only user_id 1, 2, and 3)
        for post in posts_data:
            u_id = post.get('userId')
            if u_id in [1, 2, 3]:
                cursor.execute("""
                    INSERT IGNORE INTO posts (id, user_id, title, body)
                    VALUES (%s, %s, %s, %s)
                """, (post.get('id'), u_id, post.get('title'), post.get('body')))
            conn.commit()
        print("\nTask 7: Posts for users 1, 2, and 3 added successfully.")
except Error as e:
    print(f"Database error: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
    
        

        
        
        
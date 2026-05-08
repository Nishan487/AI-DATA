import mysql.connector
from mysql.connector import Error
import requests

CITIES=[
{"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
    {"name": "Tokyo", "lat": 35.6895, "lon": 139.6917}
]

def setup_database():
    try:
        conn= mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nishan@20640904"
        )
        cursor=conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS weather_db")
        cursor.execute("USE weather_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(255) NOT NULL,
                forecast_date DATE NOT NULL,
                max_temp FLOAT NOT NULL,
                min_temp FLOAT NOT NULL
            )
        """)
        return conn,cursor
    except Error as e:
        print(f"Failed to create database: {e}")
        exit()

def fetch_store():
    conn,cursor = setup_database()
    try:
        for city in CITIES:
            name=city['name']
            lat=city['lat']
            lon=city['lon']
            url=f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
            response=requests.get(url)
            if response.status_code == 200:
                data=response.json()
                daily=data.get('daily', {})
                dates=daily.get('time', [])
                max_temps=daily.get('temperature_2m_max', [])
                min_temps=daily.get('temperature_2m_min', [])
                
                for date, max_temp, min_temp in zip(dates, max_temps, min_temps):
                    cursor.execute("""
                        INSERT INTO weather (city_name, forecast_date, max_temp, min_temp)
                        VALUES (%s, %s, %s, %s)
                    """, (name, date, max_temp, min_temp))
        conn.commit()
        print("Weather data fetched and stored successfully.")
        report_lines=["--- Weather Report ---\n"]
        cursor.execute("SELECT city_name,AVG(max_temp)as avg_max FROM weather GROUP BY city_name ORDER BY avg_max DESC LIMIT 1 ")
        q1=cursor.fetchone()
        report_lines.append(f"1. city with highest average max temp:{q1[0]}({q1[1]:.2f}°C)\n")
        
        cursor.execute("SELECT city_name,forecast_date,max_temp FROM weather ORDER BY max_temp DESC LIMIT 1")
        q2=cursor.fetchone()
        report_lines.append(f"2. Hottest day: {q2[0]} on {q2[1]} with max temp {q2[2]:.2f}°C\n")
        
        cursor.execute("SELECT city_name,forecast_date,(max_temp-min_temp) as diff FROM weather HAVING diff>10")
        q3=cursor.fetchall()
        report_lines.append(f"3. Days with temp difference >10°C:{len(q3)}\n")
        
        with open("summary.txt","w") as f:
            f.writelines(report_lines)
    except Error as e:
        print(f"Database error: {e}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
            
if __name__ == "__main__":
    fetch_store()


import urllib.request
import json
import csv
import os
import dotenv
dotenv.load_dotenv()
# Kathmandu coordinates
LATITUDE = 27.7172
LONGITUDE = 85.3240

def fetch_weather():
    url = (
        f"{os.getenv('API')}"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia/Kathmandu&forecast_days=7"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def save_csv(dates, max_temps, min_temps, filename="weather.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'max_temp_c', 'min_temp_c'])
        for d, mx, mn in zip(dates, max_temps, min_temps):
            writer.writerow([d, mx, mn])
    print(f"Saved {filename}")

def analyze(dates, max_temps, min_temps):
    hottest_idx = max_temps.index(max(max_temps))
    coldest_idx = min_temps.index(min(min_temps))

    print("\n=== Kathmandu 7-Day Forecast Analysis ===")
    print(f"Hottest day: {dates[hottest_idx]} — {max_temps[hottest_idx]}°C")
    print(f"Coldest day: {dates[coldest_idx]} — {min_temps[coldest_idx]}°C")
    print("\nFull forecast:")
    for d, mx, mn in zip(dates, max_temps, min_temps):
        print(f"  {d}: High {mx}°C / Low {mn}°C")

    return hottest_idx, coldest_idx

def save_summary(dates, max_temps, min_temps, hottest_idx, coldest_idx, filename="summary.txt"):
    lines = [
        "7-Day Weather Forecast Summary for Kathmandu",
        "=" * 45,
        f"Hottest day:  {dates[hottest_idx]} — Max Temp: {max_temps[hottest_idx]}°C",
        f"Coldest day:  {dates[coldest_idx]} — Min Temp: {min_temps[coldest_idx]}°C",
        "",
        "Daily Breakdown:",
    ]
    for d, mx, mn in zip(dates, max_temps, min_temps):
        lines.append(f"  {d}: High {mx}°C / Low {mn}°C")

    with open(filename, 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved {filename}")

if __name__ == "__main__":
    print("Fetching weather data from Open-Meteo...")
    data = fetch_weather()

    dates = data['daily']['time']
    max_temps = data['daily']['temperature_2m_max']
    min_temps = data['daily']['temperature_2m_min']

    save_csv(dates, max_temps, min_temps)
    hottest_idx, coldest_idx = analyze(dates, max_temps, min_temps)
    save_summary(dates, max_temps, min_temps, hottest_idx, coldest_idx)

    print("\nDone! Files created: weather.csv, summary.txt")

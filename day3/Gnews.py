import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("Gnews_API")
BASE_URL = "https://gnews.io/api/v4/top-headlines"
CSV_FILE = "news_data.csv"

countries = {
    "np": "Nepal",
    "in": "India",
    "us": "USA",
    "gb": "UK",
    "au": "Australia"
}

def fetch_news():
    all_data = []

    for code, name in countries.items():
        params = {
            "country": code,
            "max": 100,
            "apikey": API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if "articles" not in data:
                print(f"API error for {name}: {data}")
                continue

            articles = data.get("articles", [])

            for article in articles:
                title = article.get("title") or "N/A"
                source = article.get("source", {}).get("name") or "N/A"
                published = article.get("publishedAt") or "N/A"

                all_data.append({
                    "country": name,
                    "title": title,
                    "source": source,
                    "publishedat": published
                })

        except Exception as e:
            print(f"Error fetching {name}: {e}")

    df = pd.DataFrame(all_data)

    if df.empty:
        print("No data fetched")
    else:
        print(f"Fetched {len(df)} rows")

    return df


def save_to_csv(df):

    if df.empty:
        print("No new data to save")
        return

    if not os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, index=False)
        print("CSV created")
        return

    if os.stat(CSV_FILE).st_size == 0:
        df.to_csv(CSV_FILE, index=False)
        print("CSV rewritten")
        return

    try:
        existing = pd.read_csv(CSV_FILE)
    except Exception:
        df.to_csv(CSV_FILE, index=False)
        print("CSV recreated")
        return

    combined = pd.concat([existing, df], ignore_index=True)
    combined.drop_duplicates(subset=["title", "source"], inplace=True)
    combined.to_csv(CSV_FILE, index=False)

    print("CSV updated")


def analyze():

    if not os.path.exists(CSV_FILE):
        print("CSV does not exist")
        return

    if os.stat(CSV_FILE).st_size == 0:
        print("CSV is empty")
        return

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print("Error reading CSV:", e)
        return

    if df.empty:
        print("CSV has no rows")
        return

    df["publishedat"] = pd.to_datetime(df["publishedat"], errors="coerce", utc=True)
    df["word_count"] = df["title"].apply(lambda x: len(str(x).split()))

    print("\nMost headlines today:")
    print(df["country"].value_counts())

    print("\nAverage words per country:")
    print(df.groupby("country")["word_count"].mean())

    print("\nDuplicate headlines across countries:")
    dup = df[df.duplicated(subset=["title"], keep=False)]
    print(dup[["title", "country"]])

    print("\nTop news source:")
    print(df["source"].value_counts().head(1))

    now = datetime.now(timezone.utc)
    six_hours_ago = now - timedelta(hours=6)

    recent = df[df["publishedat"] >= six_hours_ago]
    older = df[df["publishedat"] < six_hours_ago]

    total = len(df)

    if total > 0:
        print("\nTime distribution:")
        print("Last 6 hours %:", round((len(recent) / total) * 100, 2))
        print("Older %:", round((len(older) / total) * 100, 2))

    print("\nDuplicate prevention:")
    print("drop_duplicates on title and source")

    filtered = df[df["word_count"] > 6]
    filtered.to_csv("filtered_headlines.csv", index=False)

    print("\nFiltered count (>6 words):", len(filtered))

    avg_words = df.groupby("country")["word_count"].mean()

    print("\nLongest average headline:", avg_words.idxmax())
    print("Shortest average headline:", avg_words.idxmin())


def main():
    df = fetch_news()
    save_to_csv(df)
    analyze()


if __name__ == "__main__":
    main()
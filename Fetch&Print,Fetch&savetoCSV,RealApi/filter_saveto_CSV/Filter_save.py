import requests
import csv

def fetch_and_save(url,filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            users=response.json()
            
            with open(filename, 'w',newline='',encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'title', 'body'])
                writer.writeheader()
                
                for user in users:
                    id=user.get('id')
                    title=user.get('title')
                    body=user.get('body')
                    writer.writerow({'id': id, 'title': title, 'body': body})
            print(f"Data successfully saved to {filename}")
            filtered_data=[]
            with open(filename, 'r',newline='',encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title=row.get('title')
                    if len(title)>5:
                        filtered_data.append(row)
            with open('filtered_data.csv', 'w',newline='',encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'title', 'body'])
                writer.writeheader()
                writer.writerows(filtered_data)
        else:
            print(f"Failed to fetch data,Status code: {response.status_code}")
            exit()

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
                    
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    filename = "data.csv"
    fetch_and_save(url,filename)
                
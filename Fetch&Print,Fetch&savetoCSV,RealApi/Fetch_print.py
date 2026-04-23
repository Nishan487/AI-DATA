import requests

def fetch_and_print(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            users=response.json()
            for user in users:
                name=user.get('name')
                email=user.get('email')
                city=user.get('address', {}).get('city')
                print(f"Name: {name}, Email: {email}, City: {city}")
        else:
            print(f"Failed to fetch data,Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/users"
    fetch_and_print(url)
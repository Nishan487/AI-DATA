import pandas as pd 
import requests


def analyse_userAnd_post():
    try:
        url = "https://jsonplaceholder.typicode.com/users"
        data = requests.get(url).json()
        df_user = pd.json_normalize(data)
        df_user = df_user[["id", "name","email","address.city"]]
        df_user = df_user.rename(columns={"address.city": "city"})
        # print(df_user)
        
        url_post = "https://jsonplaceholder.typicode.com/posts"
        data = requests.get(url_post).json()
        df_post = pd.DataFrame(data)
        df_post = df_post[["userId", "title"]]
        df_post= df_post.rename(columns={"userId": "id"})
        # print(df_post)
        
        merge_df = pd.merge(df_user, df_post, on="id")
        # print(merge_df)
        
        post_count = df_post.groupby("id").size().reset_index(name="post_count")
        df_user = pd.merge(df_user,post_count, on="id")
        df_user["email"] = df_user["email"].str.lower()

        df_user["name"] = df_user["name"].str.strip()

        df_user["city"] = df_user["city"].str.strip()
        print(df_user)
        
        df_user = df_user.dropna()
        merge_df = merge_df.dropna()
        
        print(df_user)
        merge_df.to_csv("merged_data.csv", index=False)
    except Exception as e:
        print("Error fetching data from API:", e)
        return None
        
if __name__ == "__main__":
    analyse_userAnd_post()
        
        
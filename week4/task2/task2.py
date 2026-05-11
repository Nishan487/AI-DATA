import pandas as pd,requests

try:
    url="https://jsonplaceholder.typicode.com/posts"
    data=requests.get(url).json()
    df=pd.DataFrame(data)
    
    df=df[["userId","id","title","body"]]
    print(df.head(100))
    
    wordcount=df["title"].str.split().str.len()
    df["word_count"]=wordcount
    df=df[df["word_count"]>=4]
    
    df["title"]=df["title"].str.strip().str.title()
    df["body"]=df["body"].str.strip()
    df.to_csv("cleaned_posts.csv",index=False)
    
    print(f"Total posts before cleaning: {len(data)}")
    print(f"Total posts after cleaning: {len(df)}")
    
    print(df.head())
except Exception as e:
    print("Error fetching data:", e)
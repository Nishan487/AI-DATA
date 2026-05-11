import pandas as pd
import numpy as np
def analyze_news_data(file_path):
    try:
        df=pd.read_csv(file_path)
        print(df.info())
        print(df.isnull().sum())
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df=df.dropna(subset=["name","score"])
        print("after dropna:",df.info())
        
        print("Duplicate:",df.duplicated().sum())
        
        print("Names:\n",df["name"])
        df["name"]=df["name"].str.lower()
        df["name"]=df["name"].str.strip().str.title()
        print("Cleaned Names:\n",df["name"])
        print("Datatypes:\n",df.dtypes)
        
        df['score'] = df['score'].astype(str).str.replace("'", "")
        df["score"]=pd.to_numeric(df["score"],errors='coerce')
        df["score"]=df["score"].fillna(0)
        print("Cleaned Data:\n",df)
        df=df[(df["score"]>=0) & (df["score"]<=100)]
        def analyze_grade(score):
            if score>=90:
                return "A"
            elif score>=75:
                return "B"
            elif score>=50:
                return "C"
            else:
                return "fail"
        df["grade"]=df["score"].apply(analyze_grade)
        df.to_csv("cleaned_students.csv",index=False)
        print(f"\nBefore cleaning: {len(pd.read_csv('messy_students.csv'))} rows")
        print(f"After cleaning: {len(df)} rows")
        print("Final Data:\n",df)
    except Exception as e:
        print("Error reading CSV:", e)
        
if __name__ == "__main__":
    analyze_news_data("messy_students.csv")
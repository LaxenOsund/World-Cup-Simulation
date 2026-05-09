import pandas as pd

def fetch_data():


    url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

    try:
        df = pd.read_csv(url)
        #Makes sure date is a datetime object
        df["date"] = pd.to_datetime(df["date"])
        
        # Filter out games that have not been played yet
        today = pd.Timestamp.today()
        df = df[df["date"] <= today]

        df = df[df["date"] >= "2010-01-01"]
        
        print(f"Hämtade {len(df)} matcher fram till {df['date'].max().date()}")
        return df   
    except Exception as e:
        print(f"couldnt fetch data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        df.to_csv("results.csv", index=False)
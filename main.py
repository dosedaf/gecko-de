import requests
import json
import datetime
import duckdb
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key', "")
url = "https://api.coingecko.com/api/v3/coins/markets"

query_params = {
    'vs_currency': 'usd'
}

def main():
    response = requests.get(url, headers={"x-cg-demo-api-key": api_key}, params=query_params)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    load = json.loads(response.text)
    print(len(load))
    data = response.json()

    filename = f'response_{timestamp}.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    conn = duckdb.connect('gecko.db')

    conn.execute(f"""
                 CREATE TABLE IF NOT EXISTS markets AS
                 SELECT * FROM read_json_auto('{filename}');
                 """)

    conn.execute(f"""
                 INSERT INTO markets
                 SELECT * FROM read_json_auto('{filename}');
                 """)

    df = conn.execute("SELECT * FROM markets").df()
    print(df)


if __name__ == "__main__":
    main()

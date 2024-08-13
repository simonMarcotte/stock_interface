import requests
import db_utils.query as db
import pandas as pd

URL = 'http://127.0.0.1:5000/get_max_growth'

if __name__ == "__main__":
    params = {'ticker': 'GOOGL',
                'date': '2024-08-08'}

    data = requests.get(URL, params)
    breakpoint()
    print(data)


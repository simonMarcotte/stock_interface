from google.cloud import bigquery
import pandas as pd

MAX_PROFITS = 'stockpipeline-431905.historical_stock_data.max_profits'

def get_valid_dates(ticker: str) -> list:
    """Get a list of dates available for a ticker in max profits table"""

    client = bigquery.Client()
    query = """
        SELECT date FROM `stockpipeline-431905.historical_stock_data.max_profits`
        WHERE ticker = @ticker
        ORDER BY date
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("ticker", "STRING", ticker)
        ]
    )

    try:
        dates = client.query(query, job_config=job_config).to_dataframe()
    except Exception as e:
        raise Exception(f"Error executing query: {e}")

    return dates['date'].tolist()

def get_max_growth(ticker: str, date: str) -> float:
    """From a specified ticker and date, find the max growth of a stock"""

    client = bigquery.Client()
    query = """
        SELECT max_profit FROM `stockpipeline-431905.historical_stock_data.max_profits`
        WHERE date = @date AND ticker = @ticker
        ORDER BY date
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("date", "STRING", date),
            bigquery.ScalarQueryParameter("ticker", "STRING", ticker)
        ]
    )

    try:
        growth = client.query(query, job_config=job_config).to_dataframe()
    except Exception as e:
        raise Exception(f"Error executing query: {e}")

    if growth.empty:
        return None

    return growth['max_profit'].iloc[0]

def get_valid_tickers() -> list:
    """Get a list of all tickers that appear in the max profits table"""
    
    client = bigquery.Client()
    query = "SELECT ticker FROM `stockpipeline-431905.historical_stock_data.max_profits`"

    try:
        tickers = client.query(query).to_dataframe()
        tickers = set(tickers['ticker'].tolist()) #remove dupes
    except Exception as e:
        raise Exception(f"Error executing query: {e}")

    return list(tickers)
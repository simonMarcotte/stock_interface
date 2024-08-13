# stock_interface Flask API
A Flask App to interface with the data generated by the stock data pipeline

## About

This is a Flask app to be used to interface with bigquery tables in viewing how much a stock has grown over the last 20 years.

To use the api, use the following URL: https://stock-interface-pz5znkql2a-uc.a.run.app/

If the service is used incorrectly, an appropriate error message will occur.

Don't even try SQL injections, I thought of that too :)

## Endpoints

This api currently features 3 endpoints:
- /avail_tickers
    - Requires: None
    - Returns: The tickers whose max growth is available to view.
    - Example Query: `/avail_tickers`
- /avail_dates
    - Requires: `ticker`: The stock of which you would like to get available dates to get max growth for.
    - Returns: Given a ticker, returns the list of available dates there are to see max growth of a stock.
    - Example Query: `/avail_dates?ticker=RMCOW`
- /get_max_growth
    - Requires
        - `ticker`: The stock of which you would like to get max growth for.
    - Optional:
        - `date`: The date of which you would like to get max growth for a given ticker. Format must be `YYYY-MM-DD`. If a date is not provided, the last available date for the given ticker will be used.
    - Returns:
        - The max growth (in US $) of a particular stock until a given date
    - Example query: `/get_max_growth?ticker=RMCOW&date=2024-08-08`

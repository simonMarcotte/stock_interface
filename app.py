import json
from flask import Flask, request, abort, Response
from flask_cors import CORS
import db_utils.query as db
import pandas as pd
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

load_dotenv()


@app.route('/get_max_growth', methods=['GET'])
def get_max_growth():
    """
        Gets the max growth for a specified ticker for a specified date.
        If the date is not given, the most recent date is used if it is available
    """
    date , ticker, max_growth= None, None, None

    if 'ticker' not in request.args:
        app.logger.error("No ticker provided")
        error_message = json.dumps({'message': "You must provide a ticker (example: 'GOOGL')."})
        abort(Response(error_message, 400))

    ticker = request.args['ticker']

    try:
        dates = db.get_valid_dates(ticker)
        app.logger.info("Dates retrieved")
    except Exception as e:
        app.logger.error(f"Error fetching dates: {str(e)}")
        error_message = json.dumps({'message': "An internal error occured while fetching dates for max growth."})
        abort(Response(error_message, 500))

    if not dates:
        error_message = json.dumps({"message": "no dates available for specified ticker"})
        abort(Response(error_message, 500))

    if 'date' not in request.args:  
        app.logger.warning("No date received - defaulting to last available date.")
        date = dates[-1]
    else:
        date = request.args['date']

    if date not in dates:
        app.logger.warning("Invalid date recieved defaulting to last available date")
        date = dates[-1]

    try:
        max_growth = db.get_max_growth(ticker, date)
        if max_growth is None:
            app.logger.warning("No growth data found for the provided ticker and date")
            error_message = json.dumps({'message': f"No growth data found for ticker {ticker} on {date}."})
            abort(Response(error_message, 404))
    except Exception as e:
        app.logger.error(f"Error fetching max growth: {str(e)}")
        error_message = json.dumps({'message': "An error occurred while fetching max growth data."})
        abort(Response(error_message, 500))
    
    ret = {
        'status': 200,
        'message': {"max_growth": max_growth,
                    "date": date}
    }

    return json.dumps(ret)


@app.route('/avail_dates', methods=['GET'])
def get_available_dates():
    """get dates available for a specific ticker"""

    if 'ticker' not in request.args:
        error_message = json.dumps({"message": "A ticker must be provided (example: 'GOOGL')."})
        abort(Response(error_message, 400))

    ticker = request.args['ticker']
    try:
        dates = db.get_valid_dates(ticker)
    except Exception as e:
        app.logger.error(f"Error fetching dates: {str(e)}")
        error_message = json.dumps({'message': "An internal error occurred while fetching dates."})
        abort(Response(error_message, 500))

    ret = {
        "status": 200,
        "message": {
            "dates": dates,
            "ticker": ticker
        }
    }

    return json.dumps(ret)


@app.route('/avail_tickers', methods = ['GET'])
def get_available_tickers():
    """Get all available tickers to get data from"""

    try:
        tickers = db.get_valid_tickers()
    except Exception as e:
        app.logger.error(f"Error fetching valid tickers: {str(e)}")
        error_message = json.dumps({'message': "An internal errored occured while fetching valid tickers."})
        abort(Response(error_message, 500))
    
    ret = {
        'status': 200,
        'message': {
            "tickers": tickers}
    }

    return json.dumps(ret)


if __name__ == '__main__':
    app.run()
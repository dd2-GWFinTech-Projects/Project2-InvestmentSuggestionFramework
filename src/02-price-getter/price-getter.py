# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi


class PriceGetter:
    def __init__(self, debug=false):
        self.debug = debug

    def get_prices(self, stock_name_list):

        # Set Alpaca API key and secret
        alpaca_api_key = os.getenv("ALPACA_API_KEY")
        alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

        # Create the Alpaca API object
        alpaca = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")

        # Format current date as ISO format
        now = pd.Timestamp("2020-10-28", tz="America/New_York").isoformat()

        # Set timeframe to '1D' for Alpaca API
        timeframe = "1D"

        stock_closing_prices = pd.DataFrame()
        for stock_name in stock_name_list:
            # Get current closing prices and append to dataset
            data = alpaca.get_barset([stock_name], timeframe, start=now, end=now).df
            stock_closing_prices[stock_name] = data[stock_name]["close"]

        return stock_closing_prices

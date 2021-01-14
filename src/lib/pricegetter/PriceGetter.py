# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi


class PriceGetter:


    def __init__(self, debug_level=0):

        self.debug_level = debug_level

        # Set Alpaca API key and secret
        self.alpaca_api_key = os.getenv("ALPACA_API_KEY")
        self.alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

        # Create the Alpaca API object
        self.alpaca = tradeapi.REST(self.alpaca_api_key, self.alpaca_secret_key, api_version="v2")


    def get_tickers(self):
        ticker_list = self.alpaca.list_assets(status="active")
        return ticker_list


    def get_prices(self, stock_ticker_list, trailing_n_days):

        # Format current date as ISO format
        # Trailing n days
        now = pd.Timestamp("2020-10-28", tz="America/New_York")#.isoformat()
        start = now - trailing_n_days

        # Set timeframe to '1D' for Alpaca API
        timeframe = "1D"

        stock_closing_prices = pd.DataFrame()
        for stock_ticker in stock_ticker_list:
            # Get current closing prices and append to dataset
            data = self.alpaca.get_barset([stock_ticker], timeframe, start=now, end=now).df
            stock_closing_prices[stock_ticker] = data[stock_ticker]["close"]

        return stock_closing_prices

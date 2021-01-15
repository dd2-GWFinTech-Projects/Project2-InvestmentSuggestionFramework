from unittest import TestCase
from ..pricegetter.PriceGetter import PriceGetter

class TestPriceGetter(TestCase):


    def test_get_tickers(self):
        price_getter = PriceGetter()
        ticker_list = price_getter.get_tickers_2()
        self.assertTrue(len(ticker_list) > 50)


    def test_2(self):
        import os
        import alpaca_trade_api as tradeapi
        import pandas as pd

        # Set Alpaca API key and secret
        alpaca_api_key = os.getenv("ALPACA_API_KEY")
        alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

        # Create the Alpaca API object
        alpaca = tradeapi.REST(
            alpaca_api_key,
            alpaca_secret_key,
            api_version="v2")
        # Format current date as ISO format
        now = pd.Timestamp("2020-10-28", tz="America/New_York").isoformat()

        # Set the tickers
        tickers = ["AGG", "SPY"]

        # Set timeframe to '1D' for Alpaca API
        timeframe = "1D"

        # Get current closing prices for SPY and AGG
        data = alpaca.get_barset(
            tickers,
            timeframe,
            start=now,
            end=now
        ).df

        # Preview DataFrame
        return data


        # alpaca_api_key = os.getenv("ALPACA_API_KEY")
        # alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
        # api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")
        # # api = tradeapi.REST()
        # # Get a list of all active assets.
        # active_assets = api.list_assets(status='active')
        # nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
        # print(nasdaq_assets)

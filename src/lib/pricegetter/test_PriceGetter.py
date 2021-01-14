from unittest import TestCase
from ..pricegetter.PriceGetter import PriceGetter

class TestPriceGetter(TestCase):
    def test_get_tickers(self):
        price_getter = PriceGetter()
        ticker_list = price_getter.get_tickers()
        self.assertTrue(len(ticker_list) > 50)

    def test_2(self):
        import os
        import alpaca_trade_api as tradeapi

        alpaca_api_key = os.getenv("ALPACA_API_KEY")
        alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

        # Create the Alpaca API object
        api = tradeapi.REST(alpaca_api_key, alpaca_secret_key, api_version="v2")
        # api = tradeapi.REST()
        # Get a list of all active assets.
        active_assets = api.list_assets(status='active')

        # Filter the assets down to just those on NASDAQ.
        nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
        print(nasdaq_assets)

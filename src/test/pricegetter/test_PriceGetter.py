from unittest import TestCase
from main.pricegetter.PriceGetter import PriceGetter


class TestPriceGetter(TestCase):


    def test_get_tickers(self):
        price_getter = PriceGetter()
        ticker_list = price_getter.get_tickers()
        self.assertTrue(len(ticker_list) > 50)


    def test_get_prices(self):
        price_getter = PriceGetter()
        stock_prices = price_getter.get_prices(stock_ticker_list=["AAPL", "BNGO", "CIIC"], trailing_n_days=100)
        self.assertEqual("AAPL", stock_prices.columns[0])
        self.assertEqual("BNGO", stock_prices.columns[1])
        self.assertGreater(60, stock_prices.shape[1])

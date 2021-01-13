from unittest import TestCase

from lib.pricegetter.PriceGetter import PriceGetter

class TestPriceGetter(TestCase):
    def test_get_prices(self):
        price_getter = PriceGetter()
        stock_prices = price_getter.get_prices(stock_name_list=["AAPL", "TSLA"])
        self.assertEqual("AAPL", stock_prices.columns[0])
        self.assertEqual("TSLA", stock_prices.columns[1])


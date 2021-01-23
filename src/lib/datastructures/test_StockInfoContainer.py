from unittest import TestCase
from ..datastructures.StockInfoContainer import StockInfoContainer
import pandas as pd


class TestStockInfoContainer(TestCase):


    def test_add_ticker(self):
        container = StockInfoContainer()
        container.add_ticker("AAPL")
        self.assertEqual("AAPL", container.get_all_tickers()[0])


    def test_add_ticker_list(self):
        container = StockInfoContainer()
        container.add_ticker_list(["AAPL", "MSFT", "TSLA"])
        all_tickers = container.get_all_tickers()
        self.assertEqual(3, len(all_tickers))
        expected_tickers = ["AAPL", "MSFT", "TSLA"]
        for ticker in expected_tickers:
            self.assertTrue(ticker in set(all_tickers))


    def test_add_stock_score(self):
        container = StockInfoContainer()
        container.add_stock_score("AAPL", "price analysis", 0.8)
        score_info = container.get_stock_score("AAPL")
        self.assertEqual("price analysis", score_info.get_analysis_source())
        self.assertEqual(0.8, score_info.get_score())
        # Validate that the tickers were registered
        self.assertEqual(1, len(container.get_all_tickers()))


    def test_add_stock_to_portfolio(self):
        container = StockInfoContainer()
        container.add_stock_to_portfolio("AAPL", 102)
        portfolio = container.get_portfolio()
        self.assertEqual(1, len(portfolio))
        self.assertEqual(102, portfolio["AAPL"])
        # Validate that the tickers were registered
        self.assertEqual(1, len(container.get_all_tickers()))

    def test_add_stock_price_history(self):
        container = StockInfoContainer()
        expected_index = [
            pd.Timestamp("01-01-2021", tz="America/New_York"),
            pd.Timestamp("01-02-2021", tz="America/New_York"),
            pd.Timestamp("01-03-2021", tz="America/New_York")
        ]
        expected_stock_price_history = pd.DataFrame({"APPL": [100.0, 101.0, 102.3], "MSFT": [56.0, 56.2, 59.3]}, index=index)
        container.add_stock_price_history(expected_stock_price_history)
        actual_stock_price_history__aapl = container.get_stock_price_history("AAPL")
        actual_stock_price_history__msft = container.get_stock_price_history("MSFT")
        actual_index = actual_stock_price_history__aapl.index
        self.assertEqual(3, actual_stock_price_history__aapl.shape[0])
        self.assertEqual(3, actual_stock_price_history__msft.shape[0])
        self.assertEqual(expected_index[0], actual_index[0])
        self.assertEqual(expected_index[1], actual_index[1])
        self.assertEqual(expected_index[2], actual_index[2])
        self.assertEqual(expected_stock_price_history["AAPL"].values[0], actual_stock_price_history__aapl.values[0])
        self.assertEqual(expected_stock_price_history["AAPL"].values[1], actual_stock_price_history__aapl.values[1])
        self.assertEqual(expected_stock_price_history["AAPL"].values[2], actual_stock_price_history__aapl.values[2])
        self.assertEqual(expected_stock_price_history["MSFT"].values[0], actual_stock_price_history__msft.values[0])
        self.assertEqual(expected_stock_price_history["MSFT"].values[1], actual_stock_price_history__msft.values[1])
        self.assertEqual(expected_stock_price_history["MSFT"].values[2], actual_stock_price_history__msft.values[2])
        # Validate that the tickers were registered
        self.assertEqual(2, len(container.get_all_tickers()))

    def test_add_stock_financial_metadata(self):
        container = StockInfoContainer()
        expected_financial_metadata = {}
        container.add_stock_financial_metadata("AAPL", expected_financial_metadata)
        # Validate that the tickers were registered
        self.assertEqual(1, len(container.get_all_tickers()))




    def test_get_all_tickers(self):

    def test_get_all_scores_single_level(self):

    def test_get_portfolio(self):

    def test_get_all_price_history(self):
        self.fail()


    def test_get_all_financial_metadata(self):
        self.fail()


    def test_get_financial_metadata(self):
        self.fail()


    def test_get_stock_scores(self):
        self.fail()


    def test_get_stock_num_shares(self):
        self.fail()


    def test_get_stock_price_history(self):
        self.fail()


    def test_get_stock_financial_metadata(self):
        self.fail()

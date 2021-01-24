from unittest import TestCase
from main.datastructures.StockInfoContainer import StockInfoContainer
import pandas as pd
from pathlib import Path


class TestStockInfoContainer(TestCase):


    def test_add_ticker(self):
        container = StockInfoContainer()
        container.add_ticker("AAPL")
        self.assertEqual("AAPL", container.get_all_tickers()[0])
        container.add_ticker("MSFT")
        container.add_ticker("TSLA")
        self.assertEqual(3, len(container.get_all_tickers()))
        container.add_ticker("AAPL")
        # Validate that the tickers were registered
        self.assertEqual(3, len(container.get_all_tickers()))


    def test_add_ticker_list(self):
        container = StockInfoContainer()
        container.add_ticker_list(["AAPL", "MSFT", "TSLA"])
        all_tickers = container.get_all_tickers()
        expected_tickers = ["AAPL", "MSFT", "TSLA"]
        for ticker in expected_tickers:
            self.assertTrue(ticker in set(all_tickers))
        # Validate that the tickers were registered
        self.assertEqual(3, len(all_tickers))


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
        file_path = Path("data/fmpcloud_sample_aapl.json")
        with open(file_path, "r") as json_file:
            expected_financial_metadata = json_file.read()
            container.add_stock_financial_metadata("AAPL", expected_financial_metadata)
            actual_financial_metadata = container.get_stock_financial_metadata("AAPL")
            self.assertEqual(expected_financial_metadata[0]["numberofsignificantvendors"], actual_financial_metadata[0]["numberofsignificantvendors"])
            self.assertEqual(expected_financial_metadata[0]["currentstateandlocaltaxexpensebenefit"], actual_financial_metadata[0]["currentstateandlocaltaxexpensebenefit"])
            self.assertEqual(expected_financial_metadata[0]["investmentincomeinterestanddividend"], actual_financial_metadata[0]["investmentincomeinterestanddividend"])
            self.assertIsNone(container.get_stock_financial_metadata("MSFT"))
            # Validate that the tickers were registered
            self.assertEqual(1, len(container.get_all_tickers()))




    def test_get_all_tickers(self):
        container = StockInfoContainer()
        container.add_ticker("AAPL")
        container.add_ticker("MSFT")
        container.add_ticker("TSLA")
        all_tickers = container.get_all_tickers()
        self.assertEqual(3, len(all_tickers))
        expected_tickers = ["AAPL", "MSFT", "TSLA"]
        for ticker in expected_tickers:
            self.assertTrue(ticker in set(all_tickers))

    def test_get_all_scores_single_level(self):
        container = StockInfoContainer()
        container.add_stock_score("AAPL", "price analysis", 0.8)
        container.add_stock_score("MSFT", "valuation analysis", 0.6)
        container.add_stock_score("TSLA", "other analysis", 0.4)
        all_scores_single_level = container.get_all_scores_single_level()
        expected_scores = {
            "AAPL": 0.8,
            "MSFT": 0.6,
            "TSLA": 0.4
        }
        expected_analysis_methods = {
            "AAPL": "price analysis",
            "MSFT": "valuation analysis",
            "TSLA": "other analysis"
        }
        self.assertEqual(3, all_scores_single_level)
        for actual_score_info in all_scores_single_level:
            ticker = actual_score_info.get_ticker()
            self.assertEqual(expected_analysis_methods[ticker], actual_score_info.get_analysis_source())
            self.assertEqual(expected_scores[ticker], actual_score_info.get_score())

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

from unittest import TestCase
from StockScoreContainer import StockScoreContainer

class TestStockScoreContainer(TestCase):

    def test_add(self):
        container = StockScoreContainer()
        self.assertEqual(len(container.stock_score_map), 0)
        container.add("AAPL", 0.95, "Price")
        container.add("TSLA", 0.98, "Price")
        container.add("AAPL", 0.95, "Valuation")
        container.add("TSLA", 0.98, "Valuation")
        container.add("BNGO", 0.30, "Price")
        self.assertEqual(len(container.stock_score_map), 2)

    def test_get_all_stockscores(self):
        container = StockScoreContainer()
        container.add("AAPL", 0.95, "Price")
        container.add("TSLA", 0.98, "Price")
        container.add("AAPL", 0.95, "Valuation")
        container.add("TSLA", 0.98, "Valuation")
        container.add("BNGO", 0.30, "Price")
        all_stockscores = container.get_all_stockscores()
        self.assertEqual(len(all_stockscores), 5)

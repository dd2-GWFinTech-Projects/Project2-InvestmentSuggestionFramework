from unittest import TestCase
from StockScoreContainer import StockScoreContainer

class TestStockScoreContainer(TestCase):

    def test_add(self):
        container = StockScoreContainer()
        self.assertEqual(len(container.stock_score_map), 0)
        self.build_container(container)
        self.assertEqual(len(container.stock_score_map), 2)

    def test_get_all_stockscores(self):
        container = StockScoreContainer()
        self.build_container(container)
        all_stockscores = container.get_all_stockscores()
        self.assertEqual(len(all_stockscores), 5)

    def build_container(self, container):
        container.add("AAPL", 0.95, "Price")
        container.add("TSLA", 0.98, "Price")
        container.add("AAPL", 0.85, "Valuation")
        container.add("TSLA", 0.84, "Valuation")
        container.add("BNGO", 0.30, "Price")

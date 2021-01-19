from ..portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from ..datastructures.StockInfoContainer import StockInfoContainer
from ..datastructures.CustomerMetrics import CustomerMetrics

class TestHelper:
    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def build_customer_metrics(self):
        customer_metrics = CustomerMetrics("Long", 5000, "Medium", "Intermediate")
        return customer_metrics

    def build_container(self):
        stock_score_container = StockInfoContainer()
        stock_score_container.add_stock_score("AAPL", 0.95, "Price")
        stock_score_container.add_stock_score("TSLA", 0.98, "Price")
        stock_score_container.add_stock_score("AAPL", 0.85, "Valuation")
        stock_score_container.add_stock_score("TSLA", 0.84, "Valuation")
        stock_score_container.add_stock_score("BNGO", 0.30, "Price")
        return stock_score_container

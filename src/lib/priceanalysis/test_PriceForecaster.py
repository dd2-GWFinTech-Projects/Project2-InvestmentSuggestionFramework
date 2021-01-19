from ..portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from ..datastructures.CustomerMetrics import CustomerMetrics
from ..datastructures.StockInfoContainer import StockInfoContainer
from unittest import TestCase
from ..priceanalysis.PriceForecaster import PriceForecaster


class TestPriceForecaster(TestCase):
    def test_generate_price_prediction(self):
        price_forecaster = PriceForecaster()
        portfolio_builder = PortfolioBuilder()
        customer_metrics = self.build_customer_metrics()
        stock_score_container = StockInfoContainer()
        self.build_container(stock_score_container)
        price_forecaster.analyze(stock_score_container)
        self.assertTrue(stock_score_container.get_stock_scores("AAPL").get_score() > 0)

    def build_container(self, container):
        container.add_stock_score("AAPL", 0.95, "Price")
        container.add_stock_score("TSLA", 0.98, "Price")
        container.add_stock_score("AAPL", 0.85, "Valuation")
        container.add_stock_score("TSLA", 0.84, "Valuation")
        container.add_stock_score("BNGO", 0.30, "Price")

    def build_customer_metrics(self):
        customer_metrics = CustomerMetrics("Long", 5000, "Medium", "Intermediate")
        return customer_metrics

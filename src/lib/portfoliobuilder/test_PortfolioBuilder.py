from unittest import TestCase
from ..portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from ..datastructures.CustomerMetrics import CustomerMetrics
from ..datastructures.StockInfoContainer import StockInfoContainer

class TestPortfolioBuilder(TestCase):


    def test_build_suggested_portfolio(self):

        portfolio_builder = PortfolioBuilder()
        customer_metrics = self.build_customer_metrics()
        stock_score_container = StockInfoContainer()
        self.build_container(stock_score_container)

        portfolio_actual = portfolio_builder.build_suggested_portfolio(customer_metrics, stock_score_container)
        portfolio_expected = "TSLA (100) - AAPL (100) - BNGO (100)"
        self.assertEqual(portfolio_expected, portfolio_actual)


    def build_container(self, container):
        container.add("AAPL", 0.95, "Price")
        container.add("TSLA", 0.98, "Price")
        container.add("AAPL", 0.85, "Valuation")
        container.add("TSLA", 0.84, "Valuation")
        container.add("BNGO", 0.30, "Price")

    def build_customer_metrics(self):
        customer_metrics = CustomerMetrics("Long", 5000, "Medium", "Intermediate")
        return customer_metrics

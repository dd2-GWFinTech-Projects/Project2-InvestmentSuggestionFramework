from unittest import TestCase
from main.portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from main.datastructures.CustomerMetrics import CustomerMetrics
from main.datastructures.StockInfoContainer import StockInfoContainer


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
        container.add_stock_score("AAPL", 0.95, "Price")
        container.add_stock_score("TSLA", 0.98, "Price")
        container.add_stock_score("AAPL", 0.85, "Valuation")
        container.add_stock_score("TSLA", 0.84, "Valuation")
        container.add_stock_score("BNGO", 0.30, "Price")

    def build_customer_metrics(self):
        customer_metrics = CustomerMetrics("Long", 5000, "Medium", "Intermediate")
        return customer_metrics


    def test_add_hedge_positions(self):
        self.fail()


    def test_transform_suggested_portfolio_str(self):
        self.fail()

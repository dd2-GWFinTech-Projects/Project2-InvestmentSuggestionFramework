from unittest import TestCase
from main.portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from main.datastructures.CustomerMetrics import CustomerMetrics
from main.datastructures.StockInfoContainer import StockInfoContainer
from test.lib.TestDataBuilder import TestDataBuilder


class TestPortfolioBuilder(TestCase):


    def test_build_suggested_portfolio(self):

        # Build test data
        test_data_builder = TestDataBuilder()
        customer_metrics = test_data_builder.build_customer_metrics()
        stock_info_container = StockInfoContainer()
        self.__build_container(stock_info_container)

        # Run the function
        portfolio_builder = PortfolioBuilder()
        portfolio_builder.build_suggested_portfolio(customer_metrics, stock_info_container)

        # Length assertions
        self.assertEqual(3, len(stock_info_container.get_all_tickers()))
        portfolio = stock_info_container.get_portfolio()
        self.assertEqual(3, len(portfolio))

        # Value assertions
        self.assertIsNotNone(portfolio["AAPL"])
        self.assertIsNotNone(portfolio["TSLA"])
        self.assertIsNotNone(portfolio["BNGO"])

        self.assertGreater(portfolio["AAPL"], 0)
        self.assertGreater(portfolio["TSLA"], 0)
        self.assertGreater(portfolio["BNGO"], 0)




        # portfolio_expected = "TSLA (100) - AAPL (100) - BNGO (100)"
        # self.assertEqual(portfolio_expected, portfolio_actual)
    #

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------


    def __build_container(self, container):
        container.add_stock_raw_score("AAPL", 0.95, "Price")
        container.add_stock_raw_score("TSLA", 0.98, "Price")
        container.add_stock_raw_score("AAPL", 0.85, "Valuation")
        container.add_stock_raw_score("TSLA", 0.84, "Valuation")
        container.add_stock_raw_score("BNGO", 0.30, "Price")


    def test_add_hedge_positions(self):
        self.fail()


    def test_transform_suggested_portfolio_str(self):
        self.fail()

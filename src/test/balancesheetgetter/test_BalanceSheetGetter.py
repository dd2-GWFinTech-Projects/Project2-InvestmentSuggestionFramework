from unittest import TestCase
from test.lib.TestDataBuilder import TestDataBuilder
from main.datastructures.StockInfoContainer import StockInfoContainer
from main.balancesheetgetter.BalanceSheetGetter import BalanceSheetGetter


class TestBalanceSheetGetter(TestCase):

    def test_get_financial_info(self):

        # Build test data
        container = StockInfoContainer()
        stock_ticker_list = ["AAPL", "BNGO"]
        container.add_ticker_list(stock_ticker_list)  # TODO Ensure MSFT, TSLA and other large stocks work...

        # Execute financial data loader
        balance_sheet_getter = BalanceSheetGetter()
        balance_sheet_getter.load_financial_info(container)

        # Assertions
        for stock_ticker in stock_ticker_list:
            actual_financial_metadata = container.get_stock_financial_metadata(stock_ticker)
            actual_financial_metadata_datamap = actual_financial_metadata.get_latest()
            self.assertIsNotNone(actual_financial_metadata_datamap["numberofsignificantvendors"])
            # TODO...not all stocks have shares outstanding in this report...
            # self.assertIsNotNone(actual_financial_metadata_datamap["sharesoutstanding"])
            # self.assertIsNotNone(actual_financial_metadata_datamap["longtermdebtcurrent"])

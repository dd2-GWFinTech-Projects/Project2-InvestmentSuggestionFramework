from pathlib import Path
import pandas as pd

class StockFinancialMetadata:

    def __init__(self, stock_ticker, data_list_map):
        """
        Construct the financial metadata data structure for one stock.
        Example: https://fmpcloud.io/api/v3/financial-statement-full-as-reported/AAPL?apikey=demo
        :param data_list_map: A list of financial mnetadata maps.
        """
        self.__stock_ticker = stock_ticker
        self.__data_list_map = data_list_map

        # Stock industries mapping
        self.__stock_industries_filepath = Path("data/stock_industries.csv")
        self.__stock_industry_dictionary = self.__load_stock_industries(self.__stock_industries_filepath)

    def get_stock_ticker(self):
        return self.__stock_ticker

    def get_latest(self):
        return self.__data_list_map[0]

    def get_industry(self):
        # return self.__stock_industry_dictionary[self.__stock_ticker]
        return "Technology"  # TODO

    def get_assets(self):
        return None

    def get_liabilities(self):
        return None

    def get_ebidtaba(self):
        return None

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    @staticmethod
    def __load_stock_industries(stock_industries_filepath):
        stock_industries_df = pd.read_csv(stock_industries_filepath)
        return stock_industries_df.to_dict()

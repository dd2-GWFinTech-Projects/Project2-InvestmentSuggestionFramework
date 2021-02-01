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


    def combine_data_list_map(self, other):

        for stock_ticker in other.__data_list_map.keys():

            # Initialize empty list
            if not stock_ticker in self.__data_list_map:
                self.__data_list_map[stock_ticker] = []

            this_size = len(self.__data_list_map[stock_ticker])
            other_size = len(other.__data_list_map[stock_ticker])

            max_size = np.max(this_size, other_size)

            for i in range(0, max_size):
                other_data_map = other.__data_list_map[stock_ticker][i]

                # Shortcut for new list entry
                if i >= this_size:
                    self.__data_list_map[stock_ticker].append(other_data_map)
                    continue

                # Destructively combine the maps (TODO does not maintain data integrity)
                for key, value in other_data_map.items():
                    self.__data_list_map[stock_ticker][i][key] = value

        return self


    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    # TODO fix dictionary to map symbol to industry
    @staticmethod
    def __load_stock_industries(stock_industries_filepath):
        stock_industries_df = pd.read_csv(stock_industries_filepath)
        return stock_industries_df.to_dict()

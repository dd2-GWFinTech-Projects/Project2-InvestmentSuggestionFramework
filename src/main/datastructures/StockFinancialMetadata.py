
class StockFinancialMetadata:

    def __init__(self, data_list_map):
        """
        Construct the financial metadata data structure.
        Example: https://fmpcloud.io/api/v3/financial-statement-full-as-reported/AAPL?apikey=demo
        :param data_list_map: A list of financial mnetadata maps.
        """
        self.__data_list_map = data_list_map

    def get_latest(self):
        return self.__data_list_map[0]

    def get_industry(self):
        return "Technology"  # TODO

    def get_assets(self):
        return None

    def get_liabilities(self):
        return None

    def get_ebidtaba(self):
        return None



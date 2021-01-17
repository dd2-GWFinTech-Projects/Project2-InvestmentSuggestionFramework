import pandas as pd
from ..datastructures.StockInfo import StockInfo

class StockInfoContainer:

    def __init__(self):
        self.stock_score_map = {}
        self.stock_num_shares = {}
        self.stock_price_history = pd.DataFrame()
        self.financial_metadata = {}




    def add_stock_score(self, ticker, score, analysis_source):
        """
        Add StockInfo for a stock with a score metric.
        :param ticker:
        :param score:
        :param analysis_source:
        :return:
        """
        if not (analysis_source in self.stock_info_map):
            self.stock_info_map[analysis_source] = []
        self.stock_info_map[analysis_source].append(StockInfo(ticker, score=score))

    # Expose stock info objects in a flat list
    def get_all_stockinfo(self):
        values_nested_list = self.stock_info_map.values()
        return [item for sublist in values_nested_list for item in sublist]


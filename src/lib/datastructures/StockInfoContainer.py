import pandas as pd
from ..datastructures.StockScore import StockScore
from ..datastructures.StockFinancialMetadata import StockFinancialMetadata
from ..datastructures.StockNumShares import StockNumShares

class StockInfoContainer:

    def __init__(self):
        self.stock_score_map = {}
        self.stock_num_shares = {}
        self.stock_price_history = pd.DataFrame()
        self.financial_metadata = {}

    # --------------------------------------------------------------------------
    # Add stock info
    # --------------------------------------------------------------------------

    def add_stock_score(self, ticker, analysis_source, score):
        """
        Add StockInfo for a stock with a score metric.
        :param ticker:
        :param analysis_source:
        :param score:
        :return:
        """
        if not (ticker in self.stock_score_map):
            self.stock_score_map[ticker] = []
        self.stock_score_map[ticker].append(StockScore(score, analysis_source))

    def add_stock_num_shares(self, ticker, num_shares):
        self.stock_num_shares[ticker] = StockNumShares(num_shares)
    def add_stock_price_history(self):
    def add_stock_financial_metadata(self):

    # --------------------------------------------------------------------------
    # Getters
    # --------------------------------------------------------------------------

    # Expose stock info objects in a flat list
    def get_all_stockinfo(self):
        values_nested_list = self.stock_info_map.values()
        return [item for sublist in values_nested_list for item in sublist]


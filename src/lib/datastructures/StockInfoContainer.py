import pandas as pd
from ..datastructures.StockScore import StockScore
from ..datastructures.StockFinancialMetadata import StockFinancialMetadata
from ..datastructures.StockNumShares import StockNumShares

class StockInfoContainer:

    def __init__(self):
        self.ticker_set = {}
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
        self.register_ticker(ticker)
        if not (ticker in self.stock_score_map):
            self.stock_score_map[ticker] = []
        self.stock_score_map[ticker].append(StockScore(score, analysis_source))

    def add_stock_num_shares(self, ticker, num_shares):
        self.stock_num_shares[ticker] = num_shares

    def add_stock_price_history(self, stock_price_history):
        self.stock_price_history = stock_price_history

    def add_stock_financial_metadata(self, ticker, stock_financial_metadata_map):
        self.register_ticker(ticker)
        self.financial_metadata[ticker] = StockFinancialMetadata(stock_financial_metadata_map)

    # --------------------------------------------------------------------------
    # Getters - All stock data
    # --------------------------------------------------------------------------

    def get_all_tickers(self):
        return self.ticker_set

    # Expose stock info objects in a flat list
    def get_all_scores_single_level(self):
        values_nested_list = self.stock_score_map.values()
        return [item for sublist in values_nested_list for item in sublist]

    def get_all_num_shares(self):
        return self.stock_num_shares

    def get_all_price_history(self):
        return self.stock_price_history

    def get_all_financial_metadata(self):
        return self.financial_metadata

    # --------------------------------------------------------------------------
    # Getters - Individual stock data
    # --------------------------------------------------------------------------

    def get_stock_scores(self, ticker):
        return self.stock_score_map[ticker]

    def get_stock_num_shares(self, ticker):
        return self.stock_num_shares[ticker]

    def get_stock_price_history(self, ticker):
        return self.stock_price_history[ticker]

    def get_stock_financial_metadata(self, ticker):
        return self.financial_metadata[ticker]

    # --------------------------------------------------------------------------
    # Helper functions
    # --------------------------------------------------------------------------

    def register_ticker(self, ticker):
        self.ticker_set.add(ticker)

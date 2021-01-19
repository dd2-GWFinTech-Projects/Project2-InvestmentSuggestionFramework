import pandas as pd
from ..datastructures.StockScore import StockScore
from ..datastructures.StockFinancialMetadata import StockFinancialMetadata


class StockInfoContainer:

    def __init__(self):
        self.__ticker_set = set()
        self.__stock_score_map = {}
        self.__portfolio = {}
        self.__stock_price_history = pd.DataFrame()
        self.__financial_metadata = {}

    # --------------------------------------------------------------------------
    # Add stock info
    # --------------------------------------------------------------------------

    def add_ticker(self, ticker):
        self.__register_ticker(ticker)

    def add_ticker_list(self, ticker_list):
        for ticker in ticker_list:
            self.__register_ticker(ticker)

    def add_stock_score(self, ticker, analysis_source, score):
        """
        Add StockInfo for a stock with a score metric.
        :param ticker:
        :param analysis_source:
        :param score:
        :return:
        """
        self.__register_ticker(ticker)
        if not (ticker in self.__stock_score_map):
            self.__stock_score_map[ticker] = []
        self.__stock_score_map[ticker].append(StockScore(score, analysis_source))

    def add_stock_to_portfolio(self, ticker, num_shares):
        self.__register_ticker(ticker)
        self.__portfolio[ticker] = num_shares

    def add_stock_price_history(self, stock_price_history):
        for stock_ticker in stock_price_history.columns:
            self.__register_ticker(stock_ticker)
        self.__stock_price_history = stock_price_history

    def add_stock_financial_metadata(self, ticker, stock_financial_metadata_map):
        self.__register_ticker(ticker)
        self.__financial_metadata[ticker] = StockFinancialMetadata(stock_financial_metadata_map)

    # --------------------------------------------------------------------------
    # Getters - All stock data
    # --------------------------------------------------------------------------

    def get_all_tickers(self):
        return self.__ticker_set

    def get_all_scores_single_level(self):
        """
        Expose stock score objects in a flat list.
        :return:
        """
        values_nested_list = self.__stock_score_map.values()
        return [item for sublist in values_nested_list for item in sublist]

    def get_portfolio(self):
        return self.__portfolio

    def get_all_price_history(self):
        return self.__stock_price_history

    def get_all_financial_metadata(self):
        return self.__financial_metadata

    # --------------------------------------------------------------------------
    # Getters - Individual stock data
    # --------------------------------------------------------------------------

    def get_stock_scores(self, ticker):
        return self.__stock_score_map[ticker]

    def get_stock_num_shares(self, ticker):
        return self.__portfolio[ticker]

    def get_stock_price_history(self, ticker):
        return self.__stock_price_history[ticker]

    def get_stock_financial_metadata(self, ticker):
        return self.__financial_metadata[ticker]

    # --------------------------------------------------------------------------
    # Helper functions
    # --------------------------------------------------------------------------

    def __register_ticker(self, ticker):
        self.__ticker_set.add(ticker)

# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import requests
import pandas as pd
import requests

from ..portfoliobuilder.PortfolioBuilder import PortfolioBuilder
from ..datastructures.StockInfoContainer import StockInfoContainer
from ..datastructures.CustomerMetrics import CustomerMetrics

class TestHelper:
    def __init__(self, debug_level=0):
        self.debug_level = debug_level

    def build_customer_metrics(self):
        customer_metrics = CustomerMetrics("Long", 5000, "Medium", "Intermediate")
        return customer_metrics

    def build_container_stocktickers(self, stock_score_container):
        if stock_score_container is None:
            stock_score_container = StockInfoContainer()
        stock_score_container.add_ticker("AAPL")
        stock_score_container.add_ticker("TSLA")
        stock_score_container.add_ticker("MSFT")

    def build_container_stockscores(self, stock_score_container):
        if stock_score_container is None:
            stock_score_container = StockInfoContainer()
        stock_score_container.add_stock_score("AAPL", 0.95, "Price")
        stock_score_container.add_stock_score("TSLA", 0.98, "Price")
        stock_score_container.add_stock_score("AAPL", 0.85, "Valuation")
        stock_score_container.add_stock_score("TSLA", 0.84, "Valuation")
        stock_score_container.add_stock_score("MSFT", 0.30, "Price")
        return stock_score_container

    def build_container_portfolio(self, stock_score_container):
        if stock_score_container is None:
            stock_score_container = StockInfoContainer()
        stock_score_container.add_stock_to_portfolio("AAPL", 100)
        stock_score_container.add_stock_to_portfolio("TSLA", 100)
        stock_score_container.add_stock_to_portfolio("MSFT", 100)

    def build_container_price_history(self, stock_score_container):
        if stock_score_container is None:
            stock_score_container = StockInfoContainer()
        self.__alpaca_api_key = os.getenv("ALPACA_API_KEY")
        self.__alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.__alpaca = tradeapi.REST(self.__alpaca_api_key, self.__alpaca_secret_key, api_version="v2")
        self.__fmp_cloud_key = '31853220bc5708a36155ca7f0481a5e0'
        now = pd.Timestamp("2020-10-28", tz="America/New_York")
        trailing_n_days = 100
        offset = pd.Timedelta(trailing_n_days, unit="days")
        start = now - offset
        timeframe = "1D"

        # Get stock prices
        stock_closing_prices_df = pd.DataFrame()
        for stock_ticker in [ "AAPL", "TSLA", "MSFT" ]:

            # Get current closing prices and append to dataset
            data = self.__alpaca.get_barset([stock_ticker], timeframe, start=start.isoformat(), end=now.isoformat()).df
            stock_closing_prices_df[stock_ticker] = data[stock_ticker]["close"]

        stock_info_container.add_stock_price_history(stock_closing_prices_df)
        return stock_info_container



        price_getter = PriceGetter()
        stock_price_history = price_getter.get_prices
        stock_score_container.add_stock_price_history()

    def build_container_financial_metadata(self, stock_score_container):
        if stock_score_container is None:
            stock_score_container = StockInfoContainer()
        stock_financial_metadata_map =
        stock_score_container.add_stock_financial_metadata("AAPL", stock_financial_metadata_map)

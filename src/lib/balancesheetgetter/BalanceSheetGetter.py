import requests
import pandas as pd
import requests
from ..datastructures.StockInfoContainer import StockInfoContainer


class BalanceSheetGetter:


    def __init__(self, debug_level=0):
        self.__debug_level = 0

        # Fmp Cloud API Key
        self.__fmp_cloud_key = '31853220bc5708a36155ca7f0481a5e0'


    def get_financial_info(self, stock_info_container):

        for stock_ticker in stock_info_container.get_all_tickers():
            try:
                stock_financial_metadata_str = requests.get(f"https://fmpcloud.io/api/v3/financial-statement-full-as-reported/{stock_ticker}?apikey={self.__fmp_cloud_key}")
                # TODO Other requests for auxilliary data?
            except:
                continue
            stock_financial_metadata_json = stock_financial_metadata_str.json()
            stock_financial_metadata = self.__process_stock_financial_metadata_json(stock_financial_metadata_json)
            stock_info_container.add_stock_financial_metadata(stock_ticker, stock_financial_metadata)

        return stock_info_container

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------


    def __process_stock_financial_metadata_json(self, stock_financial_metadata_json):

        # TODO Calculations and data aggregation?

        # marketCap
        # revenue
        # Gross_Profit_ratio
        # p_to_sales = MarketCapit / Revenue
        # price_to_sales

        #
        # price_to_sales_df['ps_average_sector'] = price_to_sales_df['price_to_sales'].mean()
        # price_to_sales_df['pscompany_vs_averagesector'] = price_to_sales_df['price_to_sales'] - price_to_sales_df[
        #     'ps_average_sector']
        # price_to_sales_df['price_as_per_average_industryPS'] = price_to_sales_df['ps_average_sector'] * \
        #                                                        price_to_sales_df['revenue']
        # price_to_sales_df['price_difference'] = price_to_sales_df['price_as_per_average_industryPS'] - \
        #                                         price_to_sales_df['Market_Capit']
        #

        # TODO Transform to dataframe? price_to_sales_df = pd.DataFrame.from_dict(financial_metadata, orient='index')

        return stock_financial_metadata_json

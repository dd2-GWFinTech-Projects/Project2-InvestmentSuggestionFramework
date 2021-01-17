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




        stock_ticker_str = requests.get(
            f'https://fmpcloud.io/api/v3/stock-screener?sector=technology&marketCapMoreThan=100000000000&limit=100&apikey={self.demo_key}')
        stock_ticker_json = stock_ticker_str.json()
        stock_ticker_list = []

        for item in stock_ticker_json:
            stock_ticker_list.append(item['symbol'])




        financial_metadata = {}
        for item in stock_ticker_list:
            try:
                # annual income statement since we need anual sales
                IS = requests.get(f'https://fmpcloud.io/api/v3/income-statement/{item}?apikey={demo}')
                IS = IS.json()
                Revenue = IS[0]['revenue']
                grossprofitratip = IS[0]['grossProfitRatio']
                # most recent market capitliazation
                MarketCapit = requests.get(f'https://fmpcloud.io/api/v3/market-capitalization/{item}?apikey={demo}')
                MarketCapit = MarketCapit.json()
                MarketCapit = MarketCapit[0]['marketCap']

                # Price to sales
                p_to_sales = MarketCapit / Revenue

                financial_metadata[item] = {}
                financial_metadata[item]['revenue'] = Revenue
                financial_metadata[item]['Gross_Profit_ratio'] = grossprofitratip
                financial_metadata[item]['price_to_sales'] = p_to_sales
                financial_metadata[item]['Market_Capit'] = MarketCapit
            except:
                pass
        print(financial_metadata)






        price_to_sales_df = pd.DataFrame.from_dict(financial_metadata, orient='index')

        price_to_sales_df['ps_average_sector'] = price_to_sales_df['price_to_sales'].mean()
        price_to_sales_df['pscompany_vs_averagesector'] = price_to_sales_df['price_to_sales'] - price_to_sales_df[
            'ps_average_sector']
        price_to_sales_df['price_as_per_average_industryPS'] = price_to_sales_df['ps_average_sector'] * \
                                                               price_to_sales_df['revenue']
        price_to_sales_df['price_difference'] = price_to_sales_df['price_as_per_average_industryPS'] - \
                                                price_to_sales_df['Market_Capit']



        return stock_info_container

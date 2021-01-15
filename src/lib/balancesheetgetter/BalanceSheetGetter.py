

class BalanceSheetGetter:


    def __init__(self, debug_level=0):
        self.debug_level = 0


    def get_financial_info(self, stock_info_container):
        import requests
        import pandas as pd

        import requests

        demo = '31853220bc5708a36155ca7f0481a5e0'

        companies = requests.get(
            f'https://fmpcloud.io/api/v3/stock-screener?sector=technology&marketCapMoreThan=100000000000&limit=100&apikey={demo}')
        companies = companies.json()
        technological_companies = []

        for item in companies:
            technological_companies.append(item['symbol'])

        print(technological_companies)

        pricetosales = {}
        for item in technological_companies:
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

                pricetosales[item] = {}
                pricetosales[item]['revenue'] = Revenue
                pricetosales[item]['Gross_Profit_ratio'] = grossprofitratip
                pricetosales[item]['price_to_sales'] = p_to_sales
                pricetosales[item]['Market_Capit'] = MarketCapit
            except:
                pass
        print(pricetosales)






        price_to_sales_df = pd.DataFrame.from_dict(pricetosales, orient='index')

        price_to_sales_df['ps_average_sector'] = price_to_sales_df['price_to_sales'].mean()
        price_to_sales_df['pscompany_vs_averagesector'] = price_to_sales_df['price_to_sales'] - price_to_sales_df[
            'ps_average_sector']
        price_to_sales_df['price_as_per_average_industryPS'] = price_to_sales_df['ps_average_sector'] * \
                                                               price_to_sales_df['revenue']
        price_to_sales_df['price_difference'] = price_to_sales_df['price_as_per_average_industryPS'] - \
                                                price_to_sales_df['Market_Capit']



        return stock_info_container

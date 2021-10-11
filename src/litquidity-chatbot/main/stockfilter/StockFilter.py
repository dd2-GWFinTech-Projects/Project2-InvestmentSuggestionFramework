class StockFilter:


    def __init__(self, debug_level=0):
        self.__debug_level = debug_level


    def filter(self, stock_info_container):
        # TODO
        # TODO Remove items with invalid financial data

        whitelist = { "AAPL", "TSLA", "BNGO" }
        old_stock_ticker_list = stock_info_container.get_all_tickers().copy()

        for stock_ticker in old_stock_ticker_list:
            if not (stock_ticker in whitelist):
                stock_info_container.remove_ticker(stock_ticker)

        return stock_info_container

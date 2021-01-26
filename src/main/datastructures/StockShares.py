
class StockShares:

    def __init__(self, ticker, num_shares):
        self.__ticker = ticker
        self.__num_shares = num_shares

    def get_ticker(self):
        return self.__ticker

    def get_num_shares(self):
        return self.__num_shares

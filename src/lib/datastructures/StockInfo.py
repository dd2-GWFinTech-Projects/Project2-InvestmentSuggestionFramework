class StockInfo:

    def __init__(self, ticker,
        score=None,
        num_shares=None,
        price_history=None,
        financial_metadata=None
    ):
        self.ticker = ticker
        self.score = None
        self.num_shares = None
        self.price_history = None
        self.financial_metadata = None

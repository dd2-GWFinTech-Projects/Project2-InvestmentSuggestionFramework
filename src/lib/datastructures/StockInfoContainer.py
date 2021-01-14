from ..datastructures.StockInfo import StockInfo

class StockInfoContainer:

    def __init__(self):
        self.stock_score_map = {}

    def add(self, ticker, score, analysis_source):
        if not (analysis_source in self.stock_score_map):
            self.stock_score_map[analysis_source] = []
        self.stock_score_map[analysis_source].append(StockInfo(ticker, score=score))

    def get_all_stockscores(self):
        values_nested_list = self.stock_score_map.values()
        return [item for sublist in values_nested_list for item in sublist]


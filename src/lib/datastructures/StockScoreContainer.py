from StockScore import StockScore

class StockScoreContainer:

    def __init__(self):
        self.stock_score_map = {}

    def add(self, ticker, score, analysis_source):
        if not analysis_source in self.stock_score_map:
            self.stock_score_map[analysis_source] = []
        else:
            self.stock_score_map[analysis_source].append(StockScore(ticker, score))

    def get_all_stockscores(self):
        return list(self.stock_score_map.values())
